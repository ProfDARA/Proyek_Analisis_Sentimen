import pandas as pd
from google_play_scraper import reviews

def scrape_reviews(app_id: str, count: int = 1000, lang: str = 'id') -> pd.DataFrame:
    result, _ = reviews(app_id, lang=lang, count=count)
    df = pd.DataFrame(result)
    df = df[['content', 'score']]
    return df

def label_sentiment(score: int) -> str:
    if score <= 2:
        return "negatif"
    elif score == 3:
        return "netral"
    else:
        return "positif"

def prepare_dataset(app_id: str, output_path: str = "dataset_labeled.csv") -> pd.DataFrame:
    df = scrape_reviews(app_id)
    df.drop_duplicates(subset=["content"], inplace=True)
    df.dropna(subset=["content"], inplace=True)
    df["label"] = df["score"].apply(label_sentiment)
    
    # Menyimpan content, score, label, dan tanggal ke dalam CSV
    df = df[["content", "score", "label", "at"]]
    df.to_csv(output_path, index=False)
    
    print(f"Dataset berhasil disimpan sebagai {output_path}")
    return df



if __name__ == "__main__":
    app_id = 'com.garena.game.codm'
    prepare_dataset(app_id)
