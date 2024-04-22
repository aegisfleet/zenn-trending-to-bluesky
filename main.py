import sys
from atproto import Client as BSClient
from g4f.client import Client as GPTClient

import zenn_utils
import bluesky_utils
import gpt_utils

def print_usage_and_exit():
    print("使用法: python main.py <ユーザーハンドル> <パスワード>")
    sys.exit(1)

def main():
    if len(sys.argv) != 3:
        print_usage_and_exit()

    user_handle, user_password = sys.argv[1], sys.argv[2]

    gpt_utils.setup_cookies()

    targets = zenn_utils.fetch_trending_articles()

    gpt_client = GPTClient()
    bs_client = BSClient()

    for full_url, title, description in targets:
        print(f"\nURL: {full_url}\nTitle: {title}")

        body_text = zenn_utils.fetch_article_content(full_url)
        retries = 0
        max_retries = 3
        while retries < max_retries:
            message = gpt_utils.get_description(
                gpt_client, 
                "この記事で何が伝えたいのか250文字以下で3行にまとめて欲しい。"
                "\n回答は日本語で強調文字は使用せず簡素にする。"
                f"\n以下に記事の内容を記載する。\n\n{body_text}"
            )
            title, _, image_url = bluesky_utils.fetch_webpage_metadata(full_url)
            post_text = bluesky_utils.format_message_with_link(
                title, full_url, "今日のZennトレンド", message
            )

            if len(post_text.build_text()) < 300:
                break

            retries += 1
            print(f"文字数が300文字を超えています。リトライ回数: {retries}")

        if retries == max_retries and len(post_text.build_text()) >= 300:
            print("300文字以内の文字を生成できませんでした。")
            continue

        print(post_text.build_text(), image_url, sep="\n")

        bluesky_utils.authenticate(bs_client, user_handle, user_password)
        embed_external = bluesky_utils.create_external_embed(
            bs_client, title, description, full_url, image_url
        )
        bluesky_utils.post(bs_client, post_text, embed_external)

if __name__ == "__main__":
    main()
