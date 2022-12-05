-- Move to .config/nvim/init.lua
-- Intended for 0.7.2 as my workplace couldn't build 0.8 

local function basic_config()
	local settings = {
		background = dark,
		encoding = "utf-8",
		hlsearch = false,
		wrap = false,
		incsearch = true,
		smartcase = true,

		ttyfast = true, -- Faster in terminal.app

		expandtab = true,
		smartindent = true,
		scrolloff = 5,
		shiftwidth = 4,
		tabstop = 4,

		number = true,
		ruler = true,
		cursorline = true,
		colorcolumn = "80",
		mouse = "",

		splitbelow = true,
		splitright = true,

		-- This is for nvim-cmp
		completeopt = {
			"menu",
			"menuone",
			"noselect",
		},
	}

	for key, value in pairs(settings) do
		vim.opt[key] = value
	end

	-- not in vim.o - do :h option-list
	vim.cmd("set nocompatible")

	-- set leader
	vim.g.mapleader = "'"

	-- Global variables
	vim.g.netrw_banner = 0
	vim.g.netrw_winsize = 25
end

local function remap(mode, input, result)
	vim.keymap.set(mode, input, result)
end

local function custom_commands()
	vim.api.nvim_create_user_command("W", "w", {})
	vim.api.nvim_create_user_command("Q", "q", {})
	vim.api.nvim_create_user_command("Wq", "wq", {})

	-- Copy and Paste
	remap("n", "<leader>y", '"+y')
	remap("v", "<leader>y", '"+y')
	remap("n", "<leader>p", ":put+<CR>", {})

	-- Tabs
	remap("n", "<leader>t", ":tabnew<CR>", {})
	remap("n", "<leader>n", ":tabnext<CR>", {})
	remap("n", "<leader>N", ":tabprev<CR>", {})

	-- Splits
	remap("n", "<leader>s", ":new<CR>")
	remap("n", "<leader>v", ":vnew<CR>")

	remap("n", "<leader>h", "<C-w>h")
	remap("n", "<leader>j", "<C-w>j")
	remap("n", "<leader>k", "<C-w>k")
	remap("n", "<leader>l", "<C-w>l")

	-- Navigation
	remap("n", "<leader>e", ":Ex<CR>")

	-- Move selected lines up/down
	remap("v", "J", ":m '>+1<CR>gv=gv")
	remap("v", "K", ":m '<-2<CR>gv=gv")
end

local function call_plugins()
	require("packer").startup(function(use)
		use("wbthomason/packer.nvim")
		use(
			"nvim-treesitter/nvim-treesitter",
			{ run = ":TSUpdate", commit = "4cccb6f494eb255b32a290d37c35ca12584c74d0" }
		)
		use("nvim-treesitter/nvim-treesitter-context")
		use("lukas-reineke/indent-blankline.nvim")
		use("nvim-lualine/lualine.nvim")
		use("lewis6991/gitsigns.nvim")
		use("numToStr/Comment.nvim")
		use("ellisonleao/glow.nvim")
		use({ "folke/tokyonight.nvim", as = "tokyonight" })
		use({ "catppuccin/nvim", as = "catppuccin" })
	end)

	local theme = "tokyonight"
	local success = pcall(vim.cmd, "colorscheme " .. theme)
	if not success then
		vim.cmd("colorscheme blue")
	end

	require("nvim-treesitter.configs").setup({
		ensure_installed = {
			"bash",
			"cmake",
			"comment",
			"cpp",
			"diff",
			"dockerfile",
			"git_rebase",
			"gitcommit",
			"help",
			"json",
			"lua",
			"make",
			"python",
			"toml",
			"vim",
			"yaml",
		},
		sync_install = false,
		highlight = { enable = true },
		incremental_selection = { enable = true },
		indent = { enable = true },
	})

	vim.opt.termguicolors = true
	vim.cmd([[highlight IndentBlanklineIndent1 guifg=#E06C75 gui=nocombine]])
	vim.cmd([[highlight IndentBlanklineIndent2 guifg=#E5C07B gui=nocombine]])
	vim.cmd([[highlight IndentBlanklineIndent3 guifg=#98C379 gui=nocombine]])
	vim.cmd([[highlight IndentBlanklineIndent4 guifg=#56B6C2 gui=nocombine]])
	vim.cmd([[highlight IndentBlanklineIndent5 guifg=#61AFEF gui=nocombine]])
	vim.cmd([[highlight IndentBlanklineIndent6 guifg=#C678DD gui=nocombine]])

	vim.opt.list = true
	vim.opt.listchars:append("space: ")

	require("indent_blankline").setup({
		space_char_blankline = " ",
		char_highlight_list = {
			"IndentBlanklineIndent1",
			"IndentBlanklineIndent2",
			"IndentBlanklineIndent3",
			"IndentBlanklineIndent4",
			"IndentBlanklineIndent5",
			"IndentBlanklineIndent6",
		},
	})

	local colors = {
		blue = "#80a0ff",
		cyan = "#79dac8",
		black = "#080808",
		white = "#c6c6c6",
		red = "#ff5189",
		violet = "#d183e8",
		grey = "#303030",
	}
	local bubbles_theme = {
		normal = {
			a = { fg = colors.black, bg = colors.violet },
			b = { fg = colors.white, bg = colors.grey },
			c = { fg = colors.black, bg = colors.black },
		},

		insert = { a = { fg = colors.black, bg = colors.blue } },
		visual = { a = { fg = colors.black, bg = colors.cyan } },
		replace = { a = { fg = colors.black, bg = colors.red } },

		inactive = {
			a = { fg = colors.white, bg = colors.black },
			b = { fg = colors.white, bg = colors.black },
			c = { fg = colors.black, bg = colors.black },
		},
	}

	require("lualine").setup({
		options = {
			theme = bubbles_theme,
			component_separators = "|",
			section_separators = { left = "", right = "" },
		},
		sections = {
			lualine_a = {
				{ "mode", separator = { left = "" }, right_padding = 2 },
			},
			lualine_b = { "filename", "branch" },
			lualine_c = { "fileformat" },
			lualine_x = {},
			lualine_y = { "filetype", "progress" },
			lualine_z = {
				{ "location", separator = { right = "" }, left_padding = 2 },
			},
		},
		inactive_sections = {
			lualine_a = { "filename" },
			lualine_b = {},
			lualine_c = {},
			lualine_x = {},
			lualine_y = {},
			lualine_z = { "location" },
		},
		tabline = {},
		extensions = {},
	})

	vim.api.nvim_set_hl(0, "StatusLine", { link = "Normal" })
	vim.api.nvim_set_hl(0, "StatusLineNC", { link = "Normal" })
end

local function init()
	basic_config()
	custom_commands()
	call_plugins()
end

init()
