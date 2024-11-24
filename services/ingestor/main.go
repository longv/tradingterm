package main

import (
	"context"
	"encoding/csv"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"strings"
	"time"

	"cloud.google.com/go/bigtable"
)

const (
	dataDir      = "./data"
	projectID    = "trading-term"
	instanceID   = "dev-bigtable-instance"
	tableName    = "trading-data-table"
	columnFamily = "attributes"
)

func main() {
	ctx := context.Background()

	client, err := bigtable.NewClient(ctx, projectID, instanceID)
	if err != nil {
		log.Fatalf("failed to create Bigtable client: %v", err)
	}
	defer client.Close()

	table := client.Open(tableName)

	err = filepath.Walk(dataDir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return fmt.Errorf("failed to access path %q: %w", path, err)
		}

		if filepath.Ext(path) == ".csv" {
			if err := processAndSaveToBigtable(ctx, path, table, columnFamily); err != nil {
				return fmt.Errorf("failed to process file %s: %w", path, err)
			}
		}

		return nil
	})

	if err != nil {
		log.Fatalf("failed to process files: %v", err)
	}

	log.Println("wrote CSV files successfully to Bigtable")
}

func processAndSaveToBigtable(
	ctx context.Context,
	filePath string,
	table *bigtable.Table,
	columnFamily string,
) error {
	log.Printf("Processing file %s...\n", filePath)

	csvFile, err := os.Open(filePath)
	if err != nil {
		return fmt.Errorf("failed to open file: %w", err)
	}
	defer csvFile.Close()

	reader := csv.NewReader(csvFile)
	reader.FieldsPerRecord = -1

	var records [][]string
	for {
		line, err := reader.Read()
		if err != nil {
			println(err.Error())
			break
		}

		// Skip lines starting with '#'
		if strings.HasPrefix(line[0], "#") {
			continue
		}

		records = append(records, line)
	}

	columnIndices := make(map[string]int)
	for i, record := range records {
		// Store header as column indices for easier access
		if i == 0 {
			for j, columnName := range record {
				columnIndices[strings.TrimSpace(columnName)] = j
			}

			continue
		}

		if record[columnIndices["Trading date"]] == "" ||
			record[columnIndices["Trading time"]] == "" ||
			record[columnIndices["Last"]] == "" {
			continue
		}

		symbolID := record[columnIndices["ID"]]
		secType := record[columnIndices["SecType"]]

		tradingTimestamp, err := convertToTimestamp(
			record[columnIndices["Trading date"]],
			record[columnIndices["Trading time"]],
		)
		if err != nil {
			return fmt.Errorf("failed to convert timestamp: %w", err)
		}

		rowKey := fmt.Sprintf("%s#%s#%s", secType, symbolID, tradingTimestamp)

		// Create a mutation for the row
		mut := bigtable.NewMutation()
		mut.Set(columnFamily, "last-price", bigtable.Now(), []byte(record[columnIndices["Last"]]))

		// Apply the mutation
		if err := table.Apply(ctx, rowKey, mut); err != nil {
			return fmt.Errorf("failed to write row %s: %w", rowKey, err)
		}
	}

	log.Printf("Processed and saved file: %s", filePath)

	return nil
}

func convertToTimestamp(dateStr, timeStr string) (int64, error) {
	dateLayout := "02-01-2006"   // For "dd-mm-YYYY"
	timeLayout := "15:04:05.000" // For "HH:MM:SS.sss"

	location, err := time.LoadLocation("Europe/Berlin") // CEST timezone
	if err != nil {
		return 0, fmt.Errorf("failed to load timezone: %w", err)
	}

	parsedDate, err := time.ParseInLocation(dateLayout, dateStr, location)
	if err != nil {
		return 0, fmt.Errorf("failed to parse date: %w", err)
	}

	parsedTime, err := time.ParseInLocation(timeLayout, timeStr, location)
	if err != nil {
		return 0, fmt.Errorf("failed to parse time: %w", err)
	}

	timestamp := time.Date(
		parsedDate.Year(),
		parsedDate.Month(),
		parsedDate.Day(),
		parsedTime.Hour(),
		parsedTime.Minute(),
		parsedTime.Second(),
		parsedTime.Nanosecond(),
		location,
	)

	return timestamp.Unix(), nil
}
