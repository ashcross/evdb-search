import { readFileSync, writeFileSync } from 'fs';
import { join } from "path";
// import data from "../../../output/energy-analysis.json";
const data = JSON.parse(readFileSync('ev_data.json', 'utf8'));


data.forEach((item) => {
    item.slug = item.model_slug;
    item.url = `https://evdb.nz/v/${item.model_slug}`;
});


const outputPath = join("./", "ev_data.json");
const content = JSON.stringify(data, null, 2);

writeFileSync(outputPath, content);