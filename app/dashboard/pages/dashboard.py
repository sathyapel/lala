from dash import html, callback, Output, Input
import dash_mantine_components as dmc
from dash import dcc
import pandas as pd
import plotly.express as px
from app.feature.data_cleaning2 import get_comments_cleaned, get_clean_stories, get_age_per_today
import datetime


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

                                 # Age distribution of kids over App block
                                 dmc.Text("Age distribution of kids over App",
                                          className="font-sans text-left lg:text-xl"),

                                 dmc.Paper(className="mx-2 my-3 grid grid-cols-4 gap-4",
                                           children=[
                                               dmc.Paper(withBorder=True, shadow="md", className="col-span-full lg:col-span-3", children=[
                                                   dmc.LoadingOverlay(
                                                   dcc.Graph(id="graph_age_over_comments", figure=self.get_age_distribution_over_comments(
                                                   ), config={"displayModeBar": False}),
                                                   id="graph_age_over_comments_loading",loaderProps={"variant": "bars", "color": "blue", "size": "md"},),

                                               ]),
                                               dmc.Stack(className="col-span-full lg:col-span-1",

                                                         justify="center",
                                                         children=[
                                                             dmc.Text("filter by",
                                                                      className="font-sans text-left lg:text-md"),

                                                             dmc.MultiSelect(id="get_age_option", data=["This year", "This Month"],

                                                                                maxSelectedValues=2,
                                                                                className="text-black"
                                                                             ),
                                                                             dmc.Text("view by",
                                                                      className="font-sans text-left lg:text-md"),
                                                             dmc.ChipGroup(
                                                                 [dmc.Chip(x, value=x) for x in [
                                                                     "Bar", "line", "funnel","histogram" ]],
                                                                 value="Bar",
                                                             id="bar_type")





                                                         ])


                                           ])



                             ], withBorder=True,
                                 className="col-span-3",
                                 p="sm", shadow="xs", radius="sm"),
                             dmc.Paper(id="users_growth_over_time",children=[
                                
                             ]
                                       ,
                                        
                                       
                                        withBorder=True,
                                       p="sm", shadow="xs", radius="sm"),
                             dmc.Paper("sample content2", withBorder=True,
                                       p="sm", shadow="xs", radius="sm"),
                             dmc.Paper("sample content3", withBorder=True,
                                       p="sm", shadow="xs", radius="sm"),
                             dmc.Paper("sample content4", withBorder=True,
                                       p="sm", shadow="xs", radius="sm")

                         ])


            ])

    def setCallbacks(self):
        @callback(
            Output("engagement_score_graph", "figure"),
            Input('app-theme', 'theme'))
        def update_engagement_score(apptheme):
            return self.draw_engagement_score(apptheme.get("colorScheme"))
        
        @callback(
            Output("graph_age_over_comments", "figure"),
            Input('app-theme', 'theme'),
            Input("get_age_option", "value"),
             Input("bar_type", "value"))
        def update_age_distribution(apptheme, selected_values,bar_type):
            print("selected_values", bar_type)
            return  self.get_age_distribution_over_comments(apptheme.get("colorScheme"), selected_values,bar_type)
    def get(self):
        self.setCallbacks()
        # self.setCallback2()
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

    def get_age_distribution_over_comments(self, theme="white", options=None,chart_type=None):
        date_format = '%Y-%m-%d'
        parent_kids_df = self.parent_kids_df
        parent_kids_df["dob"] = pd.to_datetime(
            parent_kids_df.age, format=date_format)
        parent_kids_df["age_on_today"] = parent_kids_df.dob.apply(
            get_age_per_today)

        stories = get_clean_stories('stories.csv')
        comments = get_comments_cleaned('comments.csv')
        comments_on_stories = comments.merge(stories.rename(
            columns={"id": "story_id"}), on="story_id", how="left")
        comment_with_story_and_kid_age = comments_on_stories.rename(columns={"user_id": "kid_id"}).merge(
            parent_kids_df.rename(columns={"id": "kid_id"})[["kid_id", "age_on_today"]], on="kid_id", how="left")
        age_distribution_over_comments = \
            comment_with_story_and_kid_age.age_on_today.value_counts().reset_index(name="count")

        top_age_dis_over_comments = age_distribution_over_comments[:12]
        fig1 = px.bar(age_distribution_over_comments, x="age_on_today", y="count",
                      title="Age Distribution Over kids interaction", labels={"age_on_today": "Age", },
                      template="plotly_dark" if theme == "dark" else "plotly_white")
        comment_with_story_and_kid_age["updated_at"] = pd.to_datetime(
            comment_with_story_and_kid_age["updated_at"])
        this_month_engage = comment_with_story_and_kid_age[comment_with_story_and_kid_age["updated_at"] >= datetime.datetime(
            2023, 10, 1, 0, 0, 0)]
        #current year engagement
        this_year_engage = comment_with_story_and_kid_age[comment_with_story_and_kid_age["updated_at"] >= datetime.datetime(
            2023, 1, 1, 0, 0, 0)]
        
        this_month_data = \
            this_month_engage.age_on_today.value_counts().reset_index(
                name="count").rename(columns={"count": "this_month_count"})
        this_month_data = this_month_data.sort_values(by="age_on_today")
        
        #year 
        this_year_data = \
            this_year_engage.age_on_today.value_counts().reset_index(
                name="count").rename(columns={"count": "this_year_count"})
        this_year_data = this_year_data.sort_values(by="age_on_today")


        total_engage = age_distribution_over_comments
        age_dist_total = total_engage.sort_values(
            by="age_on_today").rename(columns={"count": "total_count"})
        result = this_month_data.merge(age_dist_total, how="outer")
        result = result.loc[result["age_on_today"].isin(
            range(0, 20))].fillna(0)
        
        total_data =this_year_data.merge(result,how="outer")
        total_data1 =total_data.loc[total_data["age_on_today"].isin(range(0,20))].fillna(0)
        result =total_data1
        
        y_axis_data = ["total_count"]
        if options != None:
            for selected_value in options:
                if (selected_value == "This year"):
                    y_axis_data.append("this_year_count")
                else:
                    y_axis_data.append("this_month_count")
        if len(y_axis_data) > 0:
           
            if(chart_type=="Bar"):
                fig2 = px.bar(result, x="age_on_today", y=y_axis_data, title="Age Distribution Over kids interaction", labels={"age_on_today": "Age", "total_count": "This Year"},
                             template="plotly_dark" if theme == "dark" else "plotly_white")
            elif(chart_type=="line"):
                fig2 = px.line(result, x="age_on_today", y=y_axis_data, title="Age Distribution Over kids interaction", labels={"age_on_today": "Age", "total_count": "This Year"},
                             template="plotly_dark" if theme == "dark" else "plotly_white")
            elif(chart_type=="funnel"):
                fig2 = px.funnel(result, x="age_on_today", y=y_axis_data, title="Age Distribution Over kids interaction", labels={"age_on_today": "Age", "total_count": "This Year"},
                             template="plotly_dark" if theme == "dark" else "plotly_white")
            else:
                fig2 = px.histogram(result, x="age_on_today", y=y_axis_data, title="Age Distribution Over kids interaction",barmode="group", labels={"age_on_today": "Age", "total_count": "This Year"},
                             template="plotly_dark" if theme == "dark" else "plotly_white")
            
        else:
            age_distribution_over_comments = age_distribution_over_comments.sort_values(by="age_on_today")  
            if(chart_type=="Bar"):
                fig2 = px.bar(age_distribution_over_comments, x="age_on_today", y="count",
                      title="Age Distribution Over kids interaction", labels={"age_on_today": "Age", },
                      template="plotly_dark" if theme == "dark" else "plotly_white")
            elif(chart_type=="line"):
                fig2 = px.line(age_distribution_over_comments, x="age_on_today", y="count",
                      title="Age Distribution Over kids interaction", labels={"age_on_today": "Age", },
                      template="plotly_dark" if theme == "dark" else "plotly_white")
            elif(chart_type=="funnel"):
                fig2 = px.funnel(age_distribution_over_comments, x="age_on_today", y="count",
                      title="Age Distribution Over kids interaction", labels={"age_on_today": "Age", },
                      template="plotly_dark" if theme == "dark" else "plotly_white")
            else:
                fig2 = px.histogram(age_distribution_over_comments, x="age_on_today", y="count",
                      title="Age Distribution Over kids interaction", labels={"age_on_today": "Age", },
                      template="plotly_dark" if theme == "dark" else "plotly_white",barmode="group")
            

        fig2.update_xaxes(range=[0, 20])

        return fig2
