package main

// https://github.com/charmbracelet/bubbles/pull/207/files

import (
	"bufio"
	"fmt"
	"os"
	"os/signal"
	"strings"
	"syscall"

	"github.com/spf13/cobra"
	"golang.org/x/term"

	"github.com/charmbracelet/bubbles/textarea"
	tea "github.com/charmbracelet/bubbletea"
)

// TODO: altscreen rendering doesn't work
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

func initialModel(file string) model {
	txt := textarea.New()
	txt.Focus()
	txt.ShowLineNumbers = true

	w, h, _ := term.GetSize(0)
	txt.SetWidth(int(float64(w) * 0.8))
	txt.SetHeight(int(float64(h) *  0.8))

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
	w, h, _ := term.GetSize(0)
	return fmt.Sprintf(
		"%s%s%s\n%s%s%s",
		strings.Repeat("\n",int(float64(h) * 0.1)),
		strings.Repeat(" ",int(float64(w) * 0.1)),
		m.input.View(), 
		strings.Repeat(" ",int(float64(w) * 0.1)),
		m.alert,
		strings.Repeat("\n",int(float64(h) * 0.1)),
	)
}

func handleResizeSignal() {
	sigwinch := make(chan os.Signal, 1)
	signal.Notify(sigwinch, syscall.SIGWINCH)

	go func() {
		for range sigwinch {
			// TODO: Re-trigger m.View somehow, need to redraw
		}
	}()
}

var rootCmd = &cobra.Command{
	Use:   "go-text",
	Short: "text editor",
	Args:  cobra.MaximumNArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		if len(args) > 0 {
			filename := args[0]

			handleResizeSignal()
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
