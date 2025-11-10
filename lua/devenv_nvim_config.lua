local function basic_config()
	local settings = {
		clipboard = "unnamedplus",
		expandtab = true,
		hlsearch = false,
        inccommand = "split",
		mouse = "",
		number = true,
		scrolloff = 5,
		shiftwidth = 4,
		smartindent = true,
		splitbelow = true,
		splitright = true,
		tabstop = 4,
		wrap = false,
	}

	for key, value in pairs(settings) do
		vim.opt[key] = value
	end

	-- set leader
	vim.g.mapleader = "'"

	-- Global variables
	vim.g.netrw_banner = 0
	vim.g.netrw_winsize = 25
end

local function custom_commands()
	vim.api.nvim_create_user_command("W", "w", {})
	vim.api.nvim_create_user_command("Q", "q", {})
	vim.api.nvim_create_user_command("Wq", "wq", {})

	-- Copy and Paste
	vim.keymap.set("n", "<leader>y", '"+y')
	vim.keymap.set("v", "<leader>y", '"+y')
	vim.keymap.set("n", "<leader>p", ":put+<CR>", {})

	-- Tabs
	vim.keymap.set("n", "tt", ":tabnew<CR>", {})
	vim.keymap.set("n", "tn", ":tabnext<CR>", {})
	vim.keymap.set("n", "tp", ":tabprev<CR>", {})

	-- Splits
	vim.keymap.set("n", "<leader>s", ":new<CR>")
	vim.keymap.set("n", "<leader>v", ":vnew<CR>")

	vim.keymap.set("n", "<leader>h", "<C-w>h")
	vim.keymap.set("n", "<leader>j", "<C-w>j")
	vim.keymap.set("n", "<leader>k", "<C-w>k")
	vim.keymap.set("n", "<leader>l", "<C-w>l")

	-- Navigation
	vim.keymap.set("n", "<leader>e", ":Ex<CR>")

	-- Move selected lines up/down
	vim.keymap.set("v", "J", ":m '>+1<CR>gv=gv")
	vim.keymap.set("v", "K", ":m '<-2<CR>gv=gv")
end

local function cmp_init()
	-- Setup nvim-cmp.
	local cmp = require("cmp")

	cmp.setup({
		snippet = {
			expand = function(args)
				require("luasnip").lsp_expand(args.body) -- For `luasnip` users.
			end,
		},

		mapping = {
			["<C-n>"] = cmp.mapping(
				cmp.mapping.select_next_item(),
				{ "i", "c" }
			),
			["<C-p>"] = cmp.mapping(
				cmp.mapping.select_prev_item(),
				{ "i", "c" }
			),
			["<C-b>"] = cmp.mapping(cmp.mapping.scroll_docs(-4), { "i", "c" }),
			["<C-f>"] = cmp.mapping(cmp.mapping.scroll_docs(4), { "i", "c" }),
			["<C-Space>"] = cmp.mapping(cmp.mapping.complete(), { "i", "c" }),
			["<C-y>"] = cmp.config.disable, -- Specify `cmp.config.disable` if you want to remove the default `<C-y>` mapping.
			["<C-e>"] = cmp.mapping({
				i = cmp.mapping.abort(),
				c = cmp.mapping.close(),
			}),
			["<CR>"] = cmp.mapping.confirm({ select = true }), -- Accept currently selected item. Set `select` to `false` to only confirm explicitly selected items.
		},

		sources = cmp.config.sources({
			{ name = "nvim_lsp" },
			{ name = "luasnip" }, --TODO More luasnip stuff
		}, {
			{ name = "buffer" },
			{ name = "path" },
		}),
	})
end

local on_attach = function(client, bufnr, opts)
	-- Enable completion triggered by <c-x><c-o>
	vim.api.nvim_buf_set_option(bufnr, "omnifunc", "v:lua.vim.lsp.omnifunc")
	local opts = { noremap = true, silent = true }

	-- Mappings.
	-- See `:help vim.lsp.*` for documentation on any of the below functions
	vim.api.nvim_buf_set_keymap( bufnr, "n", "gD", "<cmd>lua vim.lsp.buf.declaration()<CR>", opts)
	vim.api.nvim_buf_set_keymap( bufnr, "n", "gd", "<cmd>lua vim.lsp.buf.definition()<CR>", opts)
	vim.api.nvim_buf_set_keymap( bufnr, "n", "K", "<cmd>lua vim.lsp.buf.hover()<CR>", opts)
	vim.api.nvim_buf_set_keymap( bufnr, "n", "gi", "<cmd>lua vim.lsp.buf.implementation()<CR>", opts)
	vim.api.nvim_buf_set_keymap( bufnr, "n", "<C-k>", "<cmd>lua vim.lsp.buf.signature_help()<CR>", opts)
	vim.api.nvim_buf_set_keymap( bufnr, "n", "<leader>wa", "<cmd>lua vim.lsp.buf.add_workspace_folder()<CR>", opts)
	vim.api.nvim_buf_set_keymap( bufnr, "n", "<leader>wr", "<cmd>lua vim.lsp.buf.remove_workspace_folder()<CR>", opts)
	vim.api.nvim_buf_set_keymap( bufnr, "n", "<leader>wl", "<cmd>lua print(vim.inspect(vim.lsp.buf.list_workspace_folders()))<CR>", opts)
	vim.api.nvim_buf_set_keymap( bufnr, "n", "<leader>D", "<cmd>lua vim.lsp.buf.type_definition()<CR>", opts)
	vim.api.nvim_buf_set_keymap( bufnr, "n", "<leader>r", "<cmd>lua vim.lsp.buf.rename()<CR>", opts)
	vim.api.nvim_buf_set_keymap( bufnr, "n", "<leader>c", "<cmd>lua vim.lsp.buf.code_action()<CR>", opts)
	vim.api.nvim_buf_set_keymap( bufnr, "n", "gr", "<cmd>lua vim.lsp.buf.references()<CR>", opts)
	vim.api.nvim_set_keymap( "n", "<leader>w", "<cmd>lua vim.diagnostic.open_float()<CR>", opts)
	vim.api.nvim_set_keymap( "n", "[d", "<cmd>lua vim.diagnostic.goto_prev()<CR>", opts)
	vim.api.nvim_set_keymap( "n", "]d", "<cmd>lua vim.diagnostic.goto_next()<CR>", opts)
	vim.api.nvim_set_keymap( "n", "<leader>q", "<cmd>lua vim.diagnostic.setloclist()<CR>", opts)

	vim.api.nvim_buf_set_keymap( bufnr, "n", "<leader>f", "<cmd>lua vim.lsp.buf.format()<CR>", opts)
end

local function lsp_setup()
	local capabilities = require("cmp_nvim_lsp").default_capabilities(
		vim.lsp.protocol.make_client_capabilities()
	)

	require("lspconfig").clangd.setup({
		on_attach = on_attach,
		capabilities = capabilities,
	})
	require("lspconfig").cmake.setup({
		on_attach = on_attach,
		capabilities = capabilities,
	})
end

local function check_installed(plug)
    local installed = pcall(require, plug)
    -- Not sure why this is backwards
    if installed then
        return false
    else
        return true
    end
end

local function call_plugins()
	local plugins_list = {
		"savq/paq-nvim",
		"neovim/nvim-lspconfig",
		"hrsh7th/nvim-cmp",
		"hrsh7th/cmp-nvim-lsp",
		"hrsh7th/cmp-buffer",
		"hrsh7th/cmp-path",
		"L3MON4D3/LuaSnip",
		"saadparwaiz1/cmp_luasnip",
		"numToStr/Comment.nvim",
		"folke/todo-comments.nvim",
	}

	require("paq"):setup({})(plugins_list)
	require("Comment").setup()
	require("todo-comments").setup()

	if check_installed("nvim-cmp") then
		cmp_init()
	end

	if check_installed("nvim-lspconfig") then
		lsp_setup()
	end
end

local function init()
	basic_config()
	custom_commands()
	call_plugins()
end

init()
