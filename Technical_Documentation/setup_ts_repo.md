# Setup a typescript repo this way:

```bash
npm init -y
npm install typescript typescript-language-server
npx tsc --init
mkdir src/ dest/
echo "dest\nnode_modules" > .gitignore
```

Add this block to the bottom of your tsconfig.json
```json
  "exclude": [
    "node_modules"
  ]
```

- The easiest way to run this is to run `npx tsc` to compile to javascript and
then open your index.html in your browser
