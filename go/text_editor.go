package main

// https://github.com/charmbracelet/bubbles/pull/207/files

import (
	"bufio"
	"fmt"
	"os"
	"strings"

	"github.com/spf13/cobra"

	"github.com/charmbracelet/bubbles/textarea"
	"github.com/charmbracelet/lipgloss"
	tea "github.com/charmbracelet/bubbletea"
)

// This is a test prototype of sorts for a text editor. It can read and write 
// to a specified file, and you can move the cursor up to edit a previous line
// Writing to earlier in a given line isn't currently supported, neither is 
// opening an empty buffer. The lipgloss styling needs work, but as that's 
// only cosmetic, I'm not going to dedicate time to that for a prototype.

type model struct {
	alert string
	current_line int
	input textarea.Model
	lines []string
	open_file string
}

func (m model) Init() tea.Cmd {
	return tea.Batch(textarea.Blink, tea.EnterAltScreen)
}

var style = lipgloss.NewStyle().
	BorderStyle(lipgloss.NormalBorder()).
	// BorderForeground(lipgloss.Color("63")).
	MarginLeft(10).
	MarginTop(5).
	Background(lipgloss.Color("#333333"))


func initialModel(file string) model {
	txt := textarea.New()
	txt.FocusedStyle.Base = style
	txt.Focus()
	txt.ShowLineNumbers = true

	var lines []string

	f, err := os.Open(file)
	if err != nil {
		f, _ := os.Create(file)
		lines = []string{""}
		defer f.Close()
	} else {
		scanner := bufio.NewScanner(f)
		for scanner.Scan() {
			lines = append(lines, scanner.Text())
		}

		if err := scanner.Err(); err != nil {
			fmt.Println("error with scanning")
		}
	}
	defer f.Close()

	txt.SetValue(strings.Join(lines, "\n"))

	return model{
		alert: "placeholder....",
		current_line: len(lines),
		input: txt,
		lines: lines,
		open_file: file,
	}
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	var tiCmd tea.Cmd
	m.input, tiCmd = m.input.Update(msg)

	switch msg := msg.(type) {
	case tea.WindowSizeMsg:
		m.input.SetWidth(int(float64(msg.Width) * 0.8))
		m.input.SetHeight(int(float64(msg.Height) *  0.8))
	case tea.KeyMsg:
		switch msg.String() {
		case "enter":
			m.lines = append(m.lines, "")
			m.current_line ++
		case ";":
			m.alert = "Command palete opened!"
		case "ctrl+c":
			return m, tea.Quit
		case "ctrl+s":
			err := os.WriteFile(m.open_file, []byte(strings.Join(m.lines, "\n")), 0644)
			if err != nil {
				m.alert = err.Error()
			} else { m.alert = "File saved!" }
		case "up":
			m.current_line--
		case "down":
			m.current_line++
		case "backspace":
			curr := m.lines[m.current_line - 1]
			m.lines[m.current_line - 1] = curr[:len(curr) - 1]
		default:
			m.lines[m.current_line - 1] += msg.String()
		}
	}

	return m, tiCmd
}

func (m model) View() string {
	return fmt.Sprintf(
		"%s\n%s",
		m.input.View(), 
		m.alert,
	)
}

var rootCmd = &cobra.Command{
	Use:   "go-text",
	Short: "text editor",
	Args:  cobra.MaximumNArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		if len(args) > 0 {
			filename := args[0]

			p := tea.NewProgram(initialModel(filename), tea.WithAltScreen())
			if err := p.Start(); err != nil {
				fmt.Printf("Alas, there's been an error: %v", err)
				os.Exit(1)
			}
		} else {
			fmt.Println("No filename provided")
		}
	},
}

func main() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}
