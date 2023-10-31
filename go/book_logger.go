package main

import (
	"fmt"
	"os"

	"github.com/spf13/cobra"
)

func create_db() {}
func db_exists() bool { return false }
func new_entry() {}
func list_reviews() {}
func new_tbr() {}
func list_tbr() {}

var review bool
var regen_db bool
var add bool

var rootCmd = &cobra.Command{
	Use:   "book-log",
	Run: func(cmd *cobra.Command, args []string) {
		if !db_exists() { create_db() }
	},
}

var logCmd = &cobra.Command{
	Use:   "review",
	Run: func(cmd *cobra.Command, args []string) {
		if add {
			new_entry()
		} else {
			list_reviews()
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
	TbrCmd.Flags().BoolVarP(&add, "add", "", false, "")

	rootCmd.AddCommand(logCmd)
	rootCmd.AddCommand(TbrCmd)

	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}
