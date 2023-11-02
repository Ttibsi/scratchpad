package main

import (
	"database/sql"
	"fmt"
	"os"
	"strconv"
	"strings"
	"time"

	_ "github.com/mattn/go-sqlite3"
	"github.com/spf13/cobra"
)

const db_name string = "book_log.db"

type BooklogItem struct {
	title string
	author_1 string
	author_2 string
	finish_date string
	review string
}

func db_exists() bool {
	_, err := os.Stat(db_name)
	if os.IsNotExist(err) {
		fmt.Println("[LOG] Database does not exist")
		return false
	}
	return true
}

func create_db() error {
	conn, err := sql.Open("sqlite3", db_name)
	if err != nil { return err }

	creation_commands := []string {
		`CREATE TABLE books (
			book_id INTEGER PRIMARY KEY AUTOINCREMENT,
			title TEXT NOT NULL,
            author_1 TEXT NOT NULL,
            author_2 TEXT
		);`,
		`CREATE TABLE tbr (
			tbr_id INTEGER PRIMARY KEY AUTOINCREMENT,
			book_id INTEGER NOT NULL,
			date TEXT,
            FOREIGN KEY(book_id) REFERENCES books(book_id)
		);`,
		`CREATE TABLE book_log (
			log_id INTEGER PRIMARY KEY AUTOINCREMENT,
			book_id INTEGER NOT NULL,
			finish_date TEXT,
			review TEXT,
            FOREIGN KEY(book_id) REFERENCES books(book_id)
		);`,
	}

	fmt.Println("[LOG] Creating database")
	for _, cmd := range creation_commands {
		conn.Exec(cmd)
	}

	conn.Close()
	return nil
}

// TODO: If this is only called in other functions that have open connections
// We want to just pass a pointer to the conn in here instead - otherwise 
// it'll probably just lock
func getBookID(name string) (int, error) {
	conn, err := sql.Open("sqlite3", db_name)
	if err != nil { return -1, err }

	statement := "SELECT book_id FROM books WHERE title = $1"
	var ret int

	row := conn.QueryRow(statement, name)
	err = row.Scan(&ret)
	conn.Close()

	if err != nil {
		return -1, err
	} else {
		return ret, nil
	}
}

func new_entry() error {
	conn, err := sql.Open("sqlite3", db_name)
	if err != nil { return err }

	var new_book string
	var authors string
	var finish string
	var finish_date string
	var review string

	fmt.Print("Enter new book name: ")
	fmt.Scanf(new_book)
	fmt.Print("Enter author names, comma separated: ")
	fmt.Scanf(authors)

	book_id, err := getBookID(new_book)
	if err != nil { return err }

	if book_id == -1 {
		author_list := strings.Split(authors, ",")
		_, err := conn.Exec(
			"INSERT INTO books VALUES (NULL, ?, ?, ?);",
			new_book,
			author_list[0],
			author_list[1],
		)
		if err != nil { return err }
	}

	// This will now return the book id because it's just been inserted to
	// the db
	book_id, err = getBookID(new_book)
	if err != nil { return err }

	fmt.Print("Enter finish date (dd/mm/yyyy) - leave empty if today: ")
	fmt.Scanf(finish)
	fmt.Print("Enter review")
	fmt.Scanf(review)

	if finish == "" {
		finish_date = time.Now().String()
	} else {
		year, _ := strconv.Atoi(finish[6:9])
		month, _ := strconv.Atoi(finish[3:4])
		day, _ := strconv.Atoi(finish[0:1])

		finish_date = time.Date(year, time.Month(month), day, 0, 0, 0, 0, time.UTC).String()
	}


	_, err = conn.Exec(
		"INSERT INTO book_log VALUES (NULL, ?, ?, ?)",
		book_id,
		finish_date,
		review,
	)
	if err != nil { return err }

	conn.Close()
	return nil
}

func show_review(id int) error {
	var log BooklogItem

	conn, err := sql.Open("sqlite3", db_name)
	if err != nil { return err }

	err = conn.QueryRow(
		"SELECT * FROM books b INNER JOIN book_log bl ON b.book_id = bl.book_id WHERE bl.log_id = ?",
		id,
		).Scan(
			&log.title, &log.author_1, &log.author_2, &log.finish_date, &log.review,
		)

	var b strings.Builder
	b.WriteString("Book: " + log.title + "\n")
	b.WriteString("Authors: " + log.author_1)
	if log.author_2 != "" {
		b.WriteString(",  " + log.author_2 + "\n")
	} else {
		b.WriteString("\n")
	} 

	b.WriteString("Finish Date: " + log.finish_date + "\n")
	b.WriteString("Review:" + log.review + "\n")
	fmt.Println(b.String())

	conn.Close()
	return nil
}

func new_tbr() error {
	conn, err := sql.Open("sqlite3", db_name)
	if err != nil { return err }

	var new_book string
	var authors string

	fmt.Print("Enter new book name: ")
	fmt.Scanf(new_book)
	fmt.Print("Enter author names, comma separated: ")
	fmt.Scanf(authors)

	book_id, err := getBookID(new_book)
	if err != nil { return err }

	if book_id == -1 {
		author_list := strings.Split(authors, ",")
		_, err := conn.Exec(
			"INSERT INTO books VALUES (NULL, ?, ?, ?);",
			new_book,
			author_list[0],
			author_list[1],
		)
		if err != nil { return err }
	}

	// This will now return the book id because it's just been inserted to
	// the db
	book_id, err = getBookID(new_book)
	if err != nil { return err }

	_, err = conn.Exec(
		"INSERT INTO tbr VALUES (NULL, ?, ?);",
		book_id,
		time.Now().String(),
	)
	if err != nil { return err }

	conn.Close()
	return nil
}

func list_tbr() error {
	conn, err := sql.Open("sqlite3", db_name)
	if err != nil { return err }



	conn.Close()
	return nil
}

var review bool
var regen_db bool
var add bool
var review_id int

var rootCmd = &cobra.Command{
	Use:   "book-log",
	Run: func(cmd *cobra.Command, args []string) {
		if !db_exists() {
			err := create_db()

			if err != nil {
				fmt.Println("[ERROR] " + err.Error())
			}
		}
	},
}

var logCmd = &cobra.Command{
	Use:   "review",
	Run: func(cmd *cobra.Command, args []string) {
		if add {
			new_entry()
		} else {
			show_review(review_id)
		}
	},
}

var TbrCmd = &cobra.Command{
	Use:   "tbr",
	Run: func(cmd *cobra.Command, args []string) {
		if add {
			new_tbr()
		} else {
			list_tbr()
		}
	},
}


func main() {
	rootCmd.Flags().BoolVarP(&review, "review", "", false, "")
	rootCmd.Flags().BoolVarP(&regen_db, "regen_db", "", false, "")
	logCmd.Flags().BoolVarP(&add, "add", "", false, "")
	logCmd.Flags().IntVarP(&review_id, "review id", "", 0, "")
	TbrCmd.Flags().BoolVarP(&add, "add", "", false, "")

	rootCmd.AddCommand(logCmd)
	rootCmd.AddCommand(TbrCmd)

	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}
