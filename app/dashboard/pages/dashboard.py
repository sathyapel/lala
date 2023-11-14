from dash import html, callback, Output, Input
import dash_mantine_components as dmc
from dash import dcc
import pandas as pd
import plotly.express as px
from app.feature.data_cleaning2 import get_comments_cleaned,get_clean_stories,get_age_per_today


class DashBoard:

    def __init__(self):
        self.parent_kids_df = pd.read_csv('parent_kids.csv')

        self.mapContainer = html.Div(
            className="", children=[
                dmc.Header(id="content_header", className="flex-row ", children=[
                    dmc.Stack(children=[
                        dmc.Text(children="Dashboard",
                                 className="font-sans text-left lg:text-2xl", p=12),]
                              )

                ], height=80),

                html.Div(id="dash_grid", className="mx-6 my-8 grid grid-cols-3 gap-3",
                         children=[
                             dmc.Paper(children=[
                                 dmc.Text("Average Engagement Score",
                                          className="font-sans text-left lg:text-xl"),
                                 dcc.Graph(id="engagement_score_graph",
                                           figure=self.draw_engagement_score())
                             ], className="col-span-3", withBorder=True,
                                 p="sm", shadow="xs", radius="sm"),
                             dmc.Paper(children=[
                                 dmc.Text("Age distribution of kids over App",
                                          className="font-sans text-left lg:text-xl"),

                                 dmc.Paper(className="mx-2 my-3 grid grid-cols-3 gap-3",
                                           children=[
                                               dmc.Paper(withBorder=False, className="col-span-2",children=[
                                                    dcc.Graph(id="graph_age_over_comments",figure=self.get_age_distribution_over_comments(),config={"displayModeBar":False})
                                               ])
                                              

                                           ])



                             ], withBorder=True,
                                 className="col-span-3",
                                 p="sm", shadow="xs", radius="sm"),
                             dmc.Paper("sample content", withBorder=True,
                                       p="sm", shadow="xs", radius="sm"),
                             dmc.Paper("sample content", withBorder=True,
                                       p="sm", shadow="xs", radius="sm"),
                             dmc.Paper("sample content", withBorder=True,
                                       p="sm", shadow="xs", radius="sm"),
                             dmc.Paper("sample content", withBorder=True,
                                       p="sm", shadow="xs", radius="sm")

                         ])


            ])

    def setCallbacks(self):
        @callback(
            Output("engagement_score_graph", "figure"),
            Output("graph_age_over_comments","figure"),
            Input('app-theme', 'theme'))
        def update_theme(apptheme):
            return self.draw_engagement_score(apptheme.get("colorScheme")),self.get_age_distribution_over_comments(apptheme.get("colorScheme"))

    def get(self):
        self.setCallbacks()
        return self.mapContainer

    def draw_engagement_score(self, theme="white"):
        date_format = "%Y-%m-%d %H:%M:%S"
        comments = get_comments_cleaned('comments.csv')
        video_likes = pd.read_csv("video_likes.csv")
        comments["date"] = pd.to_datetime(comments["updated_at"], format=date_format).apply(
            lambda timestamp: timestamp.date())
        video_likes["date"] = pd.to_datetime(
            video_likes["updated_at"], format=date_format).apply(lambda timestamp: timestamp.date())
        comment_trend = comments.groupby(['date', 'story_id']).agg(
            {"comment": "count"}).rename(columns={"comment": "comment_count"}).reset_index()
        video_trend = video_likes.groupby(['date', 'video_id']).agg(
            {'kid_id': 'count'}).rename(columns={"kid_id": "like_counts"}).reset_index()
        like_score = video_trend.date.value_counts().reset_index()
        comment_score = comment_trend.date.value_counts().reset_index()
        dialy_trend = like_score.merge(comment_score, how="outer").dropna(
        ).drop_duplicates().rename(columns={"date": "engage_count"})
        dialy_trend1 = dialy_trend.sort_values(
            by="engage_count").rename(columns={"engage_count": "date"})
        daily_trend2 = dialy_trend1.groupby(
            "date")["count"].mean().reset_index()
        fig = px.line(daily_trend2, x="date", y="count", labels={
                      "count": "Engagement Count", "date": "Date"},
                      template="plotly_dark" if theme == "dark" else "plotly_white")

        fig.add_hline(y=daily_trend2["count"].mean())

        return fig


    def get_age_distribution_over_comments(self,theme="white"):
        date_format = '%Y-%m-%d'
        parent_kids_df =self.parent_kids_df
        parent_kids_df["dob"] = pd.to_datetime(parent_kids_df.age,format=date_format)
        parent_kids_df["age_on_today"] = parent_kids_df.dob.apply(get_age_per_today)

        stories =get_clean_stories('stories.csv')
        comments = get_comments_cleaned('comments.csv')
        comments_on_stories = comments.merge(stories.rename(columns={"id":"story_id"}),on="story_id",how="left")
        comment_with_story_and_kid_age=comments_on_stories.rename(columns={"user_id":"kid_id"}).merge(
        parent_kids_df.rename(columns={"id":"kid_id"})[["kid_id","age_on_today"]],on="kid_id",how="left")
        age_distribution_over_comments = \
        comment_with_story_and_kid_age.age_on_today.value_counts().reset_index(name="count")

        top_age_dis_over_comments=age_distribution_over_comments[:12]
        fig2=px.bar(age_distribution_over_comments,x="age_on_today",y="count",
            title="Age Distribution Over kids interaction",labels={"age_on_today":"age",},
            template="plotly_dark" if theme == "dark" else "plotly_white")
        fig2.update_xaxes(range=[0,20])
        
        return fig2
