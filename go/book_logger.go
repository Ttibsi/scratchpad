package main

import (
	"bufio"
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

type tbrItem struct {
	title string
	author_1 string
	author_2 string
	added_date string
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
	fmt.Scanln(&new_book)
	fmt.Print("Enter author names, comma separated: ")
	fmt.Scanln(&authors)

	book_id, _ := getBookID(new_book)

	if book_id == -1 {
		author_list := strings.Split(authors, ",")
		_, err := conn.Exec(
			"INSERT INTO books VALUES (NULL, ?, ?, ?);",
			new_book,
			strings.TrimSpace(author_list[0]),
			strings.TrimSpace(author_list[1]),
		)
		if err != nil { return err }
	}

	// This will now return the book id because it's just been inserted to
	// the db
	book_id, _ = getBookID(new_book)

	fmt.Print("Enter finish date (dd/mm/yyyy) - leave empty if today: ")
	fmt.Scanln(&finish)
	fmt.Print("Enter review: ")

	scanner := bufio.NewScanner(os.Stdin)
	if scanner.Scan() { review = scanner.Text() }

	if finish == "" {
		finish_date = time.Now().UTC().Format("2006/01/02")
	} else {
		year, _ := strconv.Atoi(finish[6:9])
		month, _ := strconv.Atoi(finish[3:4])
		day, _ := strconv.Atoi(finish[0:1])

		finish_date = time.Date(year, time.Month(month), day, 0, 0, 0, 0, time.UTC).Format("2006/01/02")
	}


	_, err = conn.Exec(
		"INSERT INTO book_log VALUES (NULL, ?, ?, ?)",
		book_id,
		finish_date,
		review,
	)
	if err != nil { return err }
	
	// TODO: Print review ID

	conn.Close()
	return nil
}

func show_review(id int) error {
	var log BooklogItem

	conn, err := sql.Open("sqlite3", db_name)
	if err != nil {
		fmt.Println(err.Error())
		return err 
	}

	fmt.Println("id:" + strconv.Itoa(id))
	row := conn.QueryRow(
		"SELECT b.title, b.author_1, b.author_2, bl.finish_date, bl.review FROM books b INNER JOIN book_log bl ON b.book_id = bl.book_id WHERE bl.log_id = ?;",
		id,
		)

	err = row.Scan(&log.title, &log.author_1, &log.author_2, &log.finish_date, &log.review)
	if err != nil {
		fmt.Println(err.Error())
		return err 
	}

	var sb strings.Builder
	sb.WriteString("Book: " + log.title + "\n")
	sb.WriteString("Authors: " + log.author_1)
	if log.author_2 != "" {
		sb.WriteString(",  " + log.author_2 + "\n")
	} else {
		sb.WriteString("\n")
	} 

	sb.WriteString("Finish Date: " + log.finish_date + "\n")
	sb.WriteString("Review:" + log.review + "\n")
	fmt.Println(sb.String())

	conn.Close()
	return nil
}

func new_tbr() error {
	conn, err := sql.Open("sqlite3", db_name)
	if err != nil { return err }

	var new_book string
	var authors string

	fmt.Print("Enter new book name: ")
	fmt.Scanln(&new_book)
	fmt.Print("Enter author names, comma separated: ")
	fmt.Scanln(&authors)

	book_id, _ := getBookID(new_book)

	if book_id == -1 {
		author_list := strings.Split(authors, ",")
		_, err := conn.Exec(
			"INSERT INTO books VALUES (NULL, ?, ?, ?);",
			new_book,
			strings.TrimSpace(author_list[0]),
			strings.TrimSpace(author_list[1]),
		)
		if err != nil { return err }
	}

	// This will now return the book id because it's just been inserted to
	// the db
	book_id, _ = getBookID(new_book)

	_, err = conn.Exec(
		"INSERT INTO tbr VALUES (NULL, ?, ?);",
		book_id,
		time.Now().String(),
	)
	if err != nil { return err }

	conn.Close()
	return nil
}

// TODO:
func list_tbr() error {
	conn, err := sql.Open("sqlite3", db_name)
	if err != nil { return err }

	rows, err := conn.Query("SELECT")

	var tbr_list []tbrItem

	for rows.Next() {
		var t tbrItem
		err := rows.Scan(&t.title, &t.author_1, &t.author_2, &t.added_date)
		if err != nil { return err }
		tbr_list = append(tbr_list, t)
	}

	longest_name := 0

	for _, i := range tbr_list {
		if len(i.title) > longest_name { longest_name = len(i.title) }
	}

	var sb strings.Builder
	sb.WriteString("+" + strings.Repeat("-", longest_name + 2) + "+")
	for _, i := range tbr_list {
		sb.WriteString("| " + i.title + " |")
	}
	sb.WriteString("+" + strings.Repeat("-", longest_name + 2) + "+")

	fmt.Println(sb.String())

	conn.Close()
	return nil
}

// TODO:
func print_review() {}

var review bool
var regen_db bool
var add bool

var rootCmd = &cobra.Command{
	Use:   "book-logger",
	Run: func(cmd *cobra.Command, args []string) {
		if review { 
			print_review()
			return
		}

		if regen_db {
			fmt.Println("[LOG] Regenerating DB")
			err := os.Remove(db_name)
			if err != nil { fmt.Println("[ERROR](os.remove): " + err.Error()) }
			err = create_db()
			if err != nil { fmt.Println("[ERROR](create_db): " + err.Error()) }
			return
		}

		if !db_exists() {
			err := create_db()
			if err != nil { fmt.Println("[ERROR](create_db) " + err.Error()) }
		}
	},
}

var logCmd = &cobra.Command{
	Use:   "review",
	Run: func(cmd *cobra.Command, args []string) {
		if add {
			err := new_entry()
			if err != nil { fmt.Println("ERROR](new_entry): " + err.Error())}
		} else {
			review_id, err := strconv.Atoi(args[0])
			if err != nil { fmt.Println("ERROR](show_review): " + err.Error())}

			err = show_review(review_id)
			if err != nil { fmt.Println("ERROR](show_review): " + err.Error())}
		}
	},
}

var TbrCmd = &cobra.Command{
	Use:   "tbr",
	Run: func(cmd *cobra.Command, args []string) {
		if add {
			err := new_tbr()
			if err != nil { fmt.Println("ERROR](new_tbr): " + err.Error())}
		} else {
			err := list_tbr()
			if err != nil { fmt.Println("ERROR](list_tbr): " + err.Error())}
		}
	},
}


func main() {
	rootCmd.Flags().BoolVarP(&review, "review", "", false, "")
	rootCmd.Flags().BoolVarP(&regen_db, "regen-db", "", false, "")
	logCmd.Flags().BoolVarP(&add, "add", "", false, "")
	TbrCmd.Flags().BoolVarP(&add, "add", "", false, "")

	rootCmd.AddCommand(logCmd)
	rootCmd.AddCommand(TbrCmd)

	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}
