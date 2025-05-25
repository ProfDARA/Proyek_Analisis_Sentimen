import pandas as pd
from google_play_scraper import reviews


# Scraping Ulasan Aplikasi dari Google Play Store
def scrape_reviews(app_id: str, count: int = 60000, lang: str = 'id') -> pd.DataFrame:
    result, _ = reviews(app_id, lang=lang, count=count)
    df = pd.DataFrame(result)
    # bagian berisi kolom yang ingin kita ambil
    df = df[['userName', 'content', 'score', 'at']]
    return df

# bagian ini untuk memberi label pada skor
def label_sentiment(score: int) -> str:
    if score <= 2:
        return "negatif"
    elif score == 3:
        return "netral"
    else:
        return "positif"

# Fungsi untuk menyiapkan dataset
def prepare_dataset(app_id: str, output_path: str = "dataset_labeled.csv") -> pd.DataFrame:
    df = scrape_reviews(app_id)
    df.drop_duplicates(subset=["content"], inplace=True)
    df.dropna(subset=["content"], inplace=True)
    df["label"] = df["score"].apply(label_sentiment)
    
    # Menyimpan userName, content, score, label, dan tanggal (at) ke dalam CSV
    df = df[["userName", "content", "score", "label", "at"]]
    df.to_csv(output_path, index=False)
    
    # data disimpan ke dalam CSV 
    print(f"Dataset berhasil disimpan: {output_path}")
    return df

# Contoh penggunaan, saya mereview aplikasi Call of Duty Mobile misalnya
if __name__ == "__main__":
    app_id = 'com.garena.game.codm'
    prepare_dataset(app_id)