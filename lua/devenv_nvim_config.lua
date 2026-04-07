-- Move to .config/nvim/init.lua
-- 0.12-adapted config
vim.o.hlsearch = false
vim.o.wrap = false
vim.o.inccommand = "split"
vim.o.smartcase = true
vim.o.expandtab = true
vim.o.smartindent = true
vim.o.shiftwidth = 4
vim.o.tabstop = 4
vim.o.number = true
vim.o.ruler = true
vim.o.mouse = ""
vim.o.splitbelow = true
vim.o.splitright = true
vim.o.autocomplete = true
vim.o.completeopt = "fuzzy,menu,menuone,popup,noselect"

vim.pack.add {
    "https://github.com/FabijanZulj/blame.nvim",
    "https://github.com/blazkowolf/gruber-darker.nvim",
    "https://github.com/ej-shafran/compile-mode.nvim",
    "https://github.com/neovim/nvim-lspconfig",
    "https://github.com/nvim-lua/plenary.nvim",
}

vim.cmd.colorscheme("gruber-darker")

vim.g.mapleader = ";"
vim.g.netrw_banner = 0
vim.g.netrw_winsize = 25
vim.g.netrw_liststyle = 3

vim.lsp.enable("clangd")
vim.lsp.enable("basedpyright")

vim.keymap.set('v', "<leader>y", '"+y')
vim.keymap.set('n', "<leader>p", ':put+<CR>')
vim.keymap.set('n', 'tt', ':tabnew<CR>')
vim.keymap.set('n', 'tn', ':tabnext<CR>')
vim.keymap.set('n', 'tp', ':tabprev<CR>')
vim.keymap.set('n', "<leader>s", ":new<CR>")
vim.keymap.set('n', "<leader>v", ":vnew<CR>")
vim.keymap.set('n', '<leader>h', "<C-w>h")
vim.keymap.set('n', '<leader>j', "<C-w>j")
vim.keymap.set('n', '<leader>k', "<C-w>k")
vim.keymap.set('n', '<leader>l', "<C-w>l")
vim.keymap.set('n', '<leader>e', ":Ex<CR>")
vim.keymap.set('n', 'q:', "")
vim.keymap.set('v', "J", ":m '>+1<CR>gv=gv")
vim.keymap.set('v', "K", ":m '<-2<CR>gv=gv")
vim.keymap.set('n', '<leader>q', ':ccl<CR>:lcl<CR>')
vim.keymap.set('n', '<leader>w', ':lua vim.diagnostic.open_float()<CR>')

-- find
vim.o.path="**"
vim.keymap.set('n', '<leader>f', ':find ')

vim.o.grepprg = "grep -Irn "
vim.cmd(":command! -nargs=+ Grep execute 'silent grep! <args>' | copen")
vim.keymap.set('n', '<leader>g', ':Grep ')

-- Compile_mode.nvim
vim.g.compile_mode = {}
vim.keymap.set('n', '<leader>c', ":Compile<CR>")

-- buffers
vim.keymap.set('n', '<leader>b', function()
    local items = {}
    for _, b in ipairs(vim.fn.getbufinfo({ buflisted = 1 })) do
        table.insert(items, {
            bufnr    = b.bufnr,
            filename = b.name ~= '' and b.name or '[No name]',
            lnum     = 1,
            col      = 1,
            text     = string.format("%d:%s", b.bufnr, b.name),
        })
    end
    vim.fn.setloclist(0, {}, ' ', { title = 'Buffers', items = items })
    if #items > 0 then vim.cmd('lopen') end
end)

