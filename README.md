# NZ EV Finder

A searchable database of electric vehicles available in New Zealand, built with Astro, Tailwind CSS, and Alpine.js. This is built from the source data on evdb.co.nz and is acting as an advanced search page, then directing the user to the actual ev page on evdb.co.nz

## 🚀 Project Structure

```text
/
├── public/                # Static assets
├── src/
│   ├── components/        # Reusable Astro components
│   ├── data/              # EV database and data
│   ├── layouts/           # Page layouts
│   ├── pages/             # Route pages
│   └── styles/            # Global styles
└── package.json
```

## ⚡ Features

- Search and filter electric vehicles by model, brand, price, range, and other specifications
- Responsive design optimized for desktop and mobile
- Fast filtering with Alpine.js
- Built with modern web technologies (Astro 6, Tailwind CSS 4, Alpine.js)

## 🧞 Commands

All commands are run from the root of the project:

| Command           | Action                                      |
| :---------------- | :------------------------------------------ |
| `npm install`     | Installs dependencies                       |
| `npm run dev`     | Starts local dev server at `localhost:4321` |
| `npm run build`   | Build your production site to `./dist/`     |
| `npm run preview` | Preview your build locally                  |

## 🛠️ Tech Stack

- **Astro 6** - Static site generator and component framework
- **Tailwind CSS 4** - Utility-first CSS framework
- **Alpine.js** - Lightweight JavaScript for interactivity
- **Wrangler** - Cloudflare Workers CLI for deployment

## 📝 License

This project is licensed under the MIT License.
