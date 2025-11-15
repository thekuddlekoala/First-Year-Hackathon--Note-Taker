import reflex as rx

config = rx.Config(
    app_name="First_Year_Hackathon__Note_Taker",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)