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
	"golang.org/x/crypto/ssh/terminal"
)

// GOARCH=arm64 GOOS=linux go build -o booklog book_logger.go

const db_name string = "book_log.db"

type BooklogItem struct {
	title       string
	author_1    string
	author_2    string
	finish_date string
	review      string
}

type tbrItem struct {
	title      string
	author_1   string
	author_2   string
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
	if err != nil {
		return err
	}

	creation_commands := []string{
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

func getBookID(name string, conn *sql.DB) (int, error) {
	statement := "SELECT book_id FROM books WHERE title = $1"
	var ret int

	row := conn.QueryRow(statement, name)
	err := row.Scan(&ret)

	if err != nil {
		return -1, err
	} else {
		return ret, nil
	}
}

func new_entry() error {
	conn, err := sql.Open("sqlite3", db_name)
	if err != nil {
		return err
	}

	var new_book string
	var authors string
	var finish string
	var finish_date string
	var review string

	fmt.Print("Enter new book name: ")
	fmt.Scanln(&new_book)
	fmt.Print("Enter author names, comma separated: ")
	fmt.Scanln(&authors)

	book_id, _ := getBookID(new_book, conn)

	if book_id == -1 {
		author_list := []string{}

		if strings.Contains(authors, ",") {
			author_list = strings.Split(authors, ",")
		} else {
			author_list = []string{strings.TrimSpace(authors), ""}
		}
		_, err := conn.Exec(
			"INSERT INTO books VALUES (NULL, ?, ?, ?);",
			new_book,
			strings.TrimSpace(author_list[0]),
			strings.TrimSpace(author_list[1]),
		)
		if err != nil {
			return err
		}
	}

	// This will now return the book id because it's just been inserted to
	// the db
	book_id, _ = getBookID(new_book, conn)

	fmt.Print("Enter finish date (dd/mm/yyyy) - leave empty if today: ")
	fmt.Scanln(&finish)
	fmt.Print("Enter review: ")

	scanner := bufio.NewScanner(os.Stdin)
	if scanner.Scan() {
		review = scanner.Text()
	}

	if finish == "" {
		finish_date = time.Now().UTC().Format("2006/01/02")
	} else {
		year, _ := strconv.Atoi(finish[6:9])
		month, _ := strconv.Atoi(finish[3:4])
		day, _ := strconv.Atoi(finish[0:1])

		finish_date = time.Date(year, time.Month(month), day, 0, 0, 0, 0, time.UTC).Format("2006/01/02")
	}

	var inserted_id int
	res := conn.QueryRow(
		"INSERT INTO book_log VALUES (NULL, ?, ?, ?) RETURNING log_id",
		book_id,
		finish_date,
		review,
	)
	if err != nil {
		return err
	}

	err = res.Scan(&inserted_id)
	fmt.Println("Row inserted with id: ", inserted_id)

	conn.Close()
	return nil
}

func show_review(id int) error {
	var log BooklogItem

	conn, err := sql.Open("sqlite3", db_name)
	if err != nil {
		return err
	}

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

func max(x, y int) int {
	if x > y {
		return x
	} else {
		return y
	}
}

func show_all() error {
	conn, err := sql.Open("sqlite3", db_name)
	if err != nil {
		return err
	}

	var logs []BooklogItem
	rows, err := conn.Query(
		"SELECT b.title, b.author_1, b.author_2, bl.finish_date, bl.review FROM books b INNER JOIN book_log bl ON b.book_id = bl.book_id;",
	)
	if err != nil {
		return err
	}

	for rows.Next() {
		var log BooklogItem
		rows.Scan(&log.title, &log.author_1, &log.author_2, &log.finish_date, &log.review)
		logs = append(logs, log)
	}

	// get the length of the longest of each elem
	longest_title := 0
	longest_authors := 0
	longest_review := 0
	space := 0
	for _, l := range logs {
		if len(l.title) > longest_title {
			longest_title = len(l.title)
		}

		if len(l.review) > longest_review {
			longest_review = len(l.review)
		}

		if (len(l.author_1) + len(l.author_2) + 2) > longest_authors {
			longest_authors = len(l.author_1) + len(l.author_2) + 2
		}
	}

	width, _, err := terminal.GetSize(0)
	if err != nil {
		return err
	}
	title_width := width

	var sb strings.Builder
	// TODO: If entries are longer than the headings
	// TODO: right border

	if longest_title > len("Titles") {
		space = longest_title - len("Titles")
	}
	sb.WriteString("+ Titles" + strings.Repeat(" ", space) + " |")
	title_width -= space + 3 + len("Titles")

	if longest_authors > len(" Authors") {
		space = longest_authors - len(" Authors")
	}
	sb.WriteString(" Authors" + strings.Repeat(" ", space) + "|")
	title_width -= len(" Authors |")

	sb.WriteString("  Dates    |")
	title_width -= len("  Dates   |")

	if longest_review > len(" Reviews ") {
		space = longest_review - len(" Reviews ")
	}
	if longest_review > title_width+1 {
		space = title_width + 1
	}
	sb.WriteString(" Reviews ")
	title_width -= len(" Reviews +")
	sb.WriteString(strings.Repeat(" ", space) + "+")

	sb.WriteString("\n|" + strings.Repeat("-", width-2) + "|\n")

	for idx, l := range logs {
		sb.WriteString("| " + l.title + " ")
		if len(l.title) <= len(" Titles ") {
			sb.WriteString(strings.Repeat(" ", len(" Titles ") - len(l.title) - 2))
		} 

		var authors string
		authors += l.author_1
		if l.author_2 != "" {
			authors += ", " + l.author_2
		}
		sb.WriteString("| " + authors)
		if len(authors) < len(" Authors ") {
			sb.WriteString(strings.Repeat(" ", len(" Authors ") - len(authors) + 1))
		}

		sb.WriteString(" | " + l.finish_date + " | " + l.review)
		if len(l.review) < len(" Review ") {
			sb.WriteString(strings.Repeat(" ", len(" Review ") - len(l.review) ))
		}

		if idx < len(logs)+1 {
			sb.WriteString("\n")
		}
	}

	sb.WriteString("+" + strings.Repeat("-", width-2) + "|")
	fmt.Println(sb.String())

	conn.Close()
	return nil
}

func new_tbr() error {
	conn, err := sql.Open("sqlite3", db_name)
	if err != nil {
		return err
	}

	var new_book string
	var authors string

	fmt.Print("Enter new book name: ")
	fmt.Scanln(&new_book)
	fmt.Print("Enter author names, comma separated: ")
	fmt.Scanln(&authors)

	book_id, _ := getBookID(new_book, conn)

	if book_id == -1 {
		author_list := strings.Split(authors, ",")
		_, err := conn.Exec(
			"INSERT INTO books VALUES (NULL, ?, ?, ?);",
			new_book,
			strings.TrimSpace(author_list[0]),
			strings.TrimSpace(author_list[1]),
		)
		if err != nil {
			return err
		}
	}

	// This will now return the book id because it's just been inserted to
	// the db
	book_id, _ = getBookID(new_book, conn)

	var inserted_id int
	res := conn.QueryRow(
		"INSERT INTO tbr VALUES (NULL, ?, ?);",
		book_id,
		time.Now().String(),
	)
	if err != nil {
		return err
	}
	err = res.Scan(&inserted_id)
	fmt.Println("Row inserted with id: ", inserted_id)

	conn.Close()
	return nil
}

func list_tbr() error {
	conn, err := sql.Open("sqlite3", db_name)
	if err != nil {
		return err
	}

	rows, err := conn.Query("SELECT b.title, b.author_1, b.author_2, t.date FROM books b INNER JOIN tbr t ON b.book_id = t.book_id;")
	if err != nil {
		return err
	}

	var tbr_list []tbrItem

	for rows.Next() {
		var t tbrItem
		err := rows.Scan(&t.title, &t.author_1, &t.author_2, &t.added_date)
		if err != nil {
			return err
		}
		tbr_list = append(tbr_list, t)
	}

	longest_name := 0

	for _, i := range tbr_list {
		if len(i.title) > longest_name {
			longest_name = len(i.title)
		}
	}

	var sb strings.Builder
	sb.WriteString("+" + strings.Repeat("-", longest_name+2) + "+\n")
	for _, i := range tbr_list {
		sb.WriteString("| " + i.title + " |\n")
	}
	sb.WriteString("+" + strings.Repeat("-", longest_name+2) + "+")

	fmt.Println(sb.String())

	conn.Close()
	return nil
}

func print_review() error {
	conn, err := sql.Open("sqlite3", db_name)
	if err != nil {
		return err
	}

	curr_year := time.Now().Year()
	var count int
	ret := conn.QueryRow("SELECT COUNT(*) FROM book_log WHERE finish_date > ?/01/01", curr_year)
	err = ret.Scan(&count)
	if err != nil {
		return err
	}

	fmt.Println("Report year " + strconv.Itoa(curr_year))
	fmt.Println("----------------")
	fmt.Println("Books read this year: " + strconv.Itoa(count))

	conn.Close()
	return nil
}

var review bool
var regen_db bool
var add bool

var rootCmd = &cobra.Command{
	Use: "book-logger",
	Run: func(cmd *cobra.Command, args []string) {
		if review {
			print_review()
			return
		}

		if regen_db {
			fmt.Println("[LOG] Regenerating DB")
			err := os.Remove(db_name)
			if err != nil {
				fmt.Println("[ERROR](os.remove): " + err.Error())
			}
			err = create_db()
			if err != nil {
				fmt.Println("[ERROR](create_db): " + err.Error())
			}
			return
		}

		if !db_exists() {
			err := create_db()
			if err != nil {
				fmt.Println("[ERROR](create_db) " + err.Error())
			}
		}
	},
}

var logCmd = &cobra.Command{
	Use: "review",
	Run: func(cmd *cobra.Command, args []string) {
		if add {
			err := new_entry()
			if err != nil {
				fmt.Println("ERROR](new_entry): " + err.Error())
			}
		} else {
			if len(args) == 1 {
				review_id, err := strconv.Atoi(args[0])
				if err != nil {
					fmt.Println("ERROR](show_review): " + err.Error())
				}

				err = show_review(review_id)
				if err != nil {
					fmt.Println("ERROR](show_review): " + err.Error())
				}
			} else {
				err := show_all()
				if err != nil {
					fmt.Println("ERROR](show_review): " + err.Error())
				}
			}
		}
	},
}

var TbrCmd = &cobra.Command{
	Use: "tbr",
	Run: func(cmd *cobra.Command, args []string) {
		if add {
			err := new_tbr()
			if err != nil {
				fmt.Println("ERROR](new_tbr): " + err.Error())
			}
		} else {
			err := list_tbr()
			if err != nil {
				fmt.Println("ERROR](list_tbr): " + err.Error())
			}
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
