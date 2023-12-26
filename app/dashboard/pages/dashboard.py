from dash import html, callback, Output, Input, dash_table
import dash_mantine_components as dmc
from dash import dcc
import pandas as pd
import plotly.express as px
from app.feature.data_cleaning2 import *
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
from dash_iconify import DashIconify
import numpy as np
import colorcet
import datashader as ds
import plotly.graph_objects as go
import datashader.transfer_functions as tf
from colorcet import CET_R1
from pyproj import Transformer


def isodate_todate(x):
    myDate = str(x)
    date_converted = datetime.datetime.strptime(
        myDate, '%Y-%m-%d %H:%M:%S').date()

    return str(date_converted)


def get_lang_id(lang_id, lang_mapper_list):
    lng = ""
    for lang_row in lang_mapper_list:
        if int(lang_id) == int(lang_row[0]):
            lng = lang_row[1]
            break
        else:
            continue
    return lng


class DashBoard:

    def __init__(self):
        self.parent_kids_df = pd.read_csv('parent_kids.csv')
        self.lang_trend_options = {"likes": "Likes", "comments": "Comments"}

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
                                                       id="graph_age_over_comments_loading", loaderProps={"variant": "bars", "color": "blue", "size": "md"},),

                                               ]),
                                               dmc.Stack(className="col-span-full lg:col-span-1",

                                                         justify="center",
                                                         children=[
                                                             dmc.Text("Filter by",
                                                                      className="font-sans text-left lg:text-md"),

                                                             dmc.MultiSelect(id="get_age_option", data=["This year", "This Month"],

                                                                                maxSelectedValues=2,
                                                                                className="text-black"
                                                                             ),
                                                             dmc.Text("View by",
                                                                      className="font-sans text-left lg:text-md"),
                                                             dmc.ChipGroup(
                                                                 [dmc.Chip(x, value=x) for x in [
                                                                     "Bar", "line", "funnel", "histogram"]],
                                                                 value="Bar",
                                                                 id="bar_type")





                                                         ])


                                           ])



                             ], withBorder=True,
                                 className="col-span-4",
                                 p="sm", shadow="xs", radius="sm"),
                             dmc.Paper(className="col-span-4 lg:col-span-2", id="users_and_stories", children=[
                                 dmc.Text("Users current feedback on App",
                                          className="font-sans text-left lg:text-md my-4"),
                                 dcc.Graph(
                                     id=f"wordcloud_comment",
                                     figure=self.create_word_cloud(),
                                     style={"height": "250px"},
                                     config={"displayModeBar": False,
                                             "autosizable": True, "responsive": True},
                                 )
                             ],


                                 withBorder=True,
                                 p="sm", shadow="xs", radius="sm"),
                             dmc.Paper(id="table_top_stories", className="col-span-4 lg:col-span-2", withBorder=True,
                                       children=[
                                           dmc.Text("Top stories of this month",
                                                    className="font-sans text-left lg:text-md my-4"),
                                           self.create_table(
                                               self.create_top_stories())
                                       ],
                                       p="sm", shadow="xs", radius="sm"),

                             dmc.Paper(children=[
                                 dmc.Group(
                                     children=[
                                         dmc.Tooltip(
                                             multiline=True,
                                             width=220,
                                             withArrow=True,
                                             transition="fade",
                                             transitionDuration=200,
                                             label="You can select and compare values on both plots"
                                             "These plots tells you how the stories you published based on categories are trending.. ",
                                             children=[
                                                 dmc.Group(grow=False, align="left",
                                                           children=[
                                                               dmc.Text("Story Summary",
                                                                        className="w-fit font-sans text-left lg:text-lg my-2"),
                                                               dmc.ActionIcon(
                                                                   DashIconify(icon="mingcute:information-fill"), color="blue", variant="subtle"
                                                               )]
                                                           )
                                             ],
                                         )
                                     ]
                                 ),


                                 dmc.Text("please look into first sunburst trace for having count",
                                          className="font-sans text-left text-sm lg:text-sm my-2"),
                                 dmc.LoadingOverlay(
                                     children=[
                                         dcc.Graph(id="story_category_sunburst",
                                                   figure=self.create_story_trends())],
                                     id="graph_age_over_story_trend_summary", loaderProps={"variant": "bars", "color": "blue", "size": "md"})
                             ],
                                 className="col-span-4",
                                 withBorder=True,
                                 p="sm", shadow="xs", radius="sm"),



                             dmc.Paper(className="col-span-4 lg:col-span-1",
                                       children=[
                                           dmc.Text("Active users in India",
                                                    className="font-sans text-left text-sm lg:text-lg my-2"),
                                           dcc.Graph(
                                               id="india_active_users_map_box",
                                               config={"displayModeBar": False,
                                                       "autosizable": True, "responsive": True},
                                               figure=self.create_user_map_box(
                                                   self.parent_kids_df.copy(), "longitude", "latitude")
                                           )],
                                       withBorder=True,
                                       p="sm", shadow="xs", radius="sm"),

                            dmc.Paper(className="col-span-4 lg:col-span-3",
                                      children=[
                                          dmc.Stack(children=[
                                              dmc.Text("Language trends over comments",
                                                       className="font-sans text-left text-sm lg:text-lg my-2"),
                                                       dmc.ChipGroup(
                                                                 [dmc.Chip(l, value=k) for k,l in self.lang_trend_options.items()],
                                                                 value="comments",
                                                                 id="lang_trend_type_chip"),
                                              dcc.Graph(
                                                  id="language_trends_fig",
                                                  config={"displayModeBar":False,
                                                          "autosizable": True, "responsive": True},
                                                  figure=self.create_language_trend()

                                              ),
                                              ],    
                                              align="flex-start",
                                              justify="center",
                                              spacing="xs",
                                          )],
                                      withBorder=True,
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
        def update_age_distribution(apptheme, selected_values, bar_type):
            print("selected_values", bar_type)
            return self.get_age_distribution_over_comments(apptheme.get("colorScheme"), selected_values, bar_type)

        @callback(
            Output("wordcloud_comment", "figure"),
            Input('app-theme', 'theme'))
        def change_wordcloud_theme(apptheme):
            return self.create_word_cloud(apptheme.get("colorScheme"))

        @callback(Output("story_category_sunburst", "figure"),
                  Input('app-theme', 'theme'))
        def change_sunburst_theme(apptheme):
            return self.create_story_trends(apptheme.get("colorScheme"))

        @callback(Output("language_trends_fig", "figure"),
                  Input("lang_trend_type_chip","value"),
                  Input('app-theme', 'theme'))
        def change_lang_trend_theme(trend_type,apptheme):
            return self.create_language_trend(trend_type,apptheme.get("colorScheme"))

    def get(self):
        self.setCallbacks()
        # self.setCallback2()
        return self.mapContainer

    def draw_engagement_score(self,theme="white"):
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

    def get_age_distribution_over_comments(self, theme="white", options=None, chart_type=None):
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
        # current year engagement
        this_year_engage = comment_with_story_and_kid_age[comment_with_story_and_kid_age["updated_at"] >= datetime.datetime(
            2023, 1, 1, 0, 0, 0)]

        this_month_data = \
            this_month_engage.age_on_today.value_counts().reset_index(
                name="count").rename(columns={"count": "this_month_count"})
        this_month_data = this_month_data.sort_values(by="age_on_today")

        # year
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

        total_data = this_year_data.merge(result, how="outer")
        total_data1 = total_data.loc[total_data["age_on_today"].isin(
            range(0, 20))].fillna(0)
        result = total_data1

        y_axis_data = ["total_count"]
        if options != None:
            for selected_value in options:
                if (selected_value == "This year"):
                    y_axis_data.append("this_year_count")
                else:
                    y_axis_data.append("this_month_count")
        if len(y_axis_data) > 0:

            if (chart_type == "Bar"):
                fig2 = px.bar(result, x="age_on_today", y=y_axis_data, title="Age Distribution Over kids interaction", labels={"age_on_today": "Age", "total_count": "This Year"},
                              template="plotly_dark" if theme == "dark" else "plotly_white")
            elif (chart_type == "line"):
                fig2 = px.line(result, x="age_on_today", y=y_axis_data, title="Age Distribution Over kids interaction", labels={"age_on_today": "Age", "total_count": "This Year"},
                               template="plotly_dark" if theme == "dark" else "plotly_white")
            elif (chart_type == "funnel"):
                fig2 = px.funnel(result, x="age_on_today", y=y_axis_data, title="Age Distribution Over kids interaction", labels={"age_on_today": "Age", "total_count": "This Year"},
                                 template="plotly_dark" if theme == "dark" else "plotly_white")
            else:
                fig2 = px.histogram(result, x="age_on_today", y=y_axis_data, title="Age Distribution Over kids interaction", barmode="group", labels={"age_on_today": "Age", "total_count": "This Year"},
                                    template="plotly_dark" if theme == "dark" else "plotly_white")

        else:
            age_distribution_over_comments = age_distribution_over_comments.sort_values(
                by="age_on_today")
            if (chart_type == "Bar"):
                fig2 = px.bar(age_distribution_over_comments, x="age_on_today", y="count",
                              title="Age Distribution Over kids interaction", labels={"age_on_today": "Age", },
                              template="plotly_dark" if theme == "dark" else "plotly_white")
            elif (chart_type == "line"):
                fig2 = px.line(age_distribution_over_comments, x="age_on_today", y="count",
                               title="Age Distribution Over kids interaction", labels={"age_on_today": "Age", },
                               template="plotly_dark" if theme == "dark" else "plotly_white")
            elif (chart_type == "funnel"):
                fig2 = px.funnel(age_distribution_over_comments, x="age_on_today", y="count",
                                 title="Age Distribution Over kids interaction", labels={"age_on_today": "Age", },
                                 template="plotly_dark" if theme == "dark" else "plotly_white")
            else:
                fig2 = px.histogram(age_distribution_over_comments, x="age_on_today", y="count",
                                    title="Age Distribution Over kids interaction", labels={"age_on_today": "Age", },
                                    template="plotly_dark" if theme == "dark" else "plotly_white", barmode="group")

        fig2.update_xaxes(range=[0, 20])

        return fig2

    def create_word_cloud(self, theme="dark"):
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
        comment_by_age = comment_with_story_and_kid_age.groupby(
            ['age_on_today', 'comment'])['comment'].count()
        comment_by_age = comment_by_age.reset_index(name="count")

        comment_by_age = comment_by_age["comment"].value_counts().reset_index()
        print(comment_by_age.head(4))
        comment_corpus = comment_by_age["comment"]
        comment_corpus_lower = comment_corpus.apply(
            lambda x: x.lower().split())
        comment_str_list = list(comment_corpus_lower)
        custom_stop_words = STOPWORDS.add("lala")
        comment_word_list = comment_corpus_lower.explode(
        ).value_counts().reset_index(name="count")
        print(comment_word_list.head(4))
        wordslist = " ".join(list(comment_word_list["comment"]))
        word_colud = WordCloud(collocations=False, background_color='black',
                               stopwords=custom_stop_words).generate(wordslist)
        fig = px.imshow(
            word_colud, template="plotly_dark" if theme == "dark" else "plotly_white")
        fig.update_layout(coloraxis_showscale=False)
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)
        return self.generate_wordcloud_div(custom_stop_words, wordslist, "comment", theme)

    def generate_wordcloud_fig(self, wordcloud_image, theme):
        back_color = "black" if theme == "dark" else "#F9F9FA"
        fig = px.imshow(wordcloud_image)
        fig.update_layout(
            xaxis={'visible': False},
            yaxis={'visible': False},
            margin={'t': 0, 'b': 0, 'l': 0, 'r': 0},
            hovermode=False,
            paper_bgcolor=back_color,
            plot_bgcolor=back_color,
        )
        return fig

    def generate_wordcloud_div(self, wordcloud_exclusions, words, archetype_or_group, theme):

        # save classname
        archetype_or_group = str(archetype_or_group)

        # add search query to list of exclusions
        excluded_words = wordcloud_exclusions
        back_color = "black" if theme == "dark" else "#F9F9FA"

        # instantiate wordcloud
        wordcloud = WordCloud(
            stopwords=excluded_words,
            min_font_size=8,
            scale=2.5,
            background_color=back_color,
            collocations=True,
            regexp=r"[a-zA-z#&]+",
            max_words=30,
            min_word_length=4,

            collocation_threshold=3)

        # generate image
        wordcloud_text = words
        wordcloud_image = wordcloud.generate(wordcloud_text)
        wordcloud_image = wordcloud_image.to_array()
        fig = self.generate_wordcloud_fig(wordcloud_image, theme)

        return fig

    def create_table(self, df):

        columns, values = df.columns, df.values
        header = [html.Tr([html.Th(col) for col in columns])]
        rows = [html.Tr([html.Td(cell) for cell in row]) for row in values]
        table1 = [html.Thead(header), html.Tbody(rows)]
        # dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])
        return dmc.Table(table1, horizontalSpacing=5, withColumnBorders=True, withBorder=True, highlightOnHover=True, striped=True)

    def create_top_stories(self):
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
        comment_with_story_and_kid_age["updated_at"] = pd.to_datetime(
            comment_with_story_and_kid_age["updated_at"])
        comment_with_story_and_kid_age["updated_date"] = pd.to_datetime(
            comment_with_story_and_kid_age["updated_at"].dt.date)

        this_month_stories = comment_with_story_and_kid_age[comment_with_story_and_kid_age["updated_at"] >= pd.Timestamp(
            2023, 10, 1)].groupby(["updated_date", "title"])["title"].count().reset_index(name="frequency")
        idx_max = this_month_stories.groupby(["updated_date"])[
            "frequency"].idxmax()
        this_month_top_stories = this_month_stories.loc[idx_max].sort_values(
            by='frequency', ascending=False).head()
        this_month_top_stories["updated_date"] = this_month_top_stories["updated_date"].apply(
            isodate_todate)
        # this_month_top_stories["updated_date"] = pd.to_datetime(this_month_top_stories["updated_date"].dt.date)
        return this_month_top_stories[["updated_date", "title"]]

    def create_story_trends(self, apptheme="dark"):
        date_format = '%Y-%m-%d'
        parent_kids_df = self.parent_kids_df
        video_likes = pd.read_csv("video_likes.csv")
        video_likes_kids = video_likes.merge(parent_kids_df.rename(columns={"id": "kid_id"})[["kid_id", "age_on_today"]],
                                             on="kid_id", how="left").dropna()
        parent_kids_df["dob"] = pd.to_datetime(
            parent_kids_df.age, format=date_format)
        parent_kids_df["age_on_today"] = parent_kids_df.dob.apply(
            get_age_per_today)

        stories = get_clean_stories('stories.csv')
        comments = get_comments_cleaned('comments.csv')
        categories = get_clean_categories("category.csv")
        stories2 = map_category_id_with_categories(stories, categories)

        langs = pd.read_csv("language.csv")
        langs = langs[langs["deleted_at"].isnull()]
        language_ids = langs["id"].tolist()
        lang_codes = langs["name"].to_list()
        lang_id_codes = dict(zip(language_ids, lang_codes))

        comments_on_stories = comments.merge(stories.rename(
            columns={"id": "story_id"}), on="story_id", how="left")
        comment_with_story_and_kid_age = comments_on_stories.rename(columns={"user_id": "kid_id"}).merge(
            parent_kids_df.rename(columns={"id": "kid_id"})[["kid_id", "age_on_today"]], on="kid_id", how="left")
        comment_withoutna = comment_with_story_and_kid_age.dropna()
        story_likes = video_likes.video_id.value_counts().reset_index(name="count")
        top_10_like_count = story_likes.count()[0]//10
        most_liked_stories_indices = story_likes[:top_10_like_count]
        most_liked_stories = stories[stories["id"].isin(
            list(most_liked_stories_indices["video_id"]))]
        comment_group_based_on_story = comments_on_stories.story_id.value_counts(
        ).reset_index(name="count")
        top_10_comment_count = comment_group_based_on_story.shape[0]//10
        most_comments_indices = comment_group_based_on_story[:top_10_comment_count]
        print("most_comment_indices-->", most_comments_indices.columns)
        most_commented_stories = stories[stories["id"].isin(
            list(most_comments_indices["story_id"]))]

        top_stories = pd.concat(
            [most_commented_stories, most_liked_stories]).drop_duplicates()
        top_stories = map_category_id_with_categories(top_stories, categories)
        comment_withoutna["lang_str"] = comment_withoutna["language"].apply(
            lambda langcode: lang_id_codes.get(int(langcode)))
        comment_trend_df = comment_withoutna.merge(stories2.rename(columns={"id": "story_id"})[
                                                   ["story_id", "cat_category"]], on="story_id", how="left")
        video_cat_trend_df = video_likes_kids.rename(columns={"video_id": "story_id"}).merge(stories2.rename(
            columns={"id": "story_id"})[["story_id", "cat_category", "language"]], on="story_id", how="left")
        video_cat_trend_df["lang_str"] = video_cat_trend_df.dropna()["language"].apply(
            lambda langcode: lang_id_codes.get(int(langcode)))
        stories2["lang_str"] = stories2["language"].apply(
            lambda langcode: lang_id_codes.get(int(langcode)))
        like_trend_df = video_cat_trend_df[[
            "story_id", "lang_str", "cat_category", "age_on_today"]]
        interactive_df = pd.concat([comment_trend_df, like_trend_df])
        print("interactive_df", stories2.columns)
        inter_df = interactive_df[["lang_str", "cat_category", "age_on_today"]]
        stories_cats_df = stories2[["lang_str", "cat_category"]]
        categories_trend_df = inter_df.groupby(
            'lang_str').value_counts().reset_index()
        stories_published_df = stories_cats_df.groupby(
            'lang_str').value_counts().reset_index()
        print("categories df-->", categories_trend_df.columns)
        print("categories df-->", stories_published_df.columns)
        column_titles_in_fig = [
            "Category based children count", "Category based story count"]
        sb1 = px.sunburst(categories_trend_df, path=[
                          "lang_str", "cat_category", "age_on_today"], values="count", color_discrete_sequence=px.colors.qualitative.Antique)
        sb2 = px.sunburst(stories_published_df, path=[
                          "lang_str", "cat_category",], values="count")
        fig = make_subplots(rows=1, cols=2, specs=[
            [{"type": "sunburst"}, {"type": "sunburst"}]
        ], column_titles=column_titles_in_fig, start_cell='bottom-left')

        fig.add_trace(sb1.data[0], row=1, col=1)
        fig.add_trace(sb2.data[0], row=1, col=2)
        javascript_code = """
            function updateAnnotationPosition() {
            var width = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
    
            if (width <= 600) {  // Adjust the threshold as needed
                Plotly.update('story_category_sunburst', {
            'annotations[0].y': -0.1,  // Adjust the y position for mobile
            'annotations[1].y': -0.1   // Adjust the y position for mobile
             });
            }
        }

        // Attach the callback to window resize event
        window.addEventListener('resize', updateAnnotationPosition);

        // Initial call to set the annotation positions based on the initial resolution
        updateAnnotationPosition();
        """
        fig.for_each_annotation(lambda a:  a.update(
            y=-0.2) if a.text in column_titles_in_fig else a.update(x=0.0))

        # set the colorways to set the initial colors in plots
        fig.update_layout(
            {"template": "plotly_dark" if apptheme == 'dark' else "plotly_white", "colorway": ["#FECB52", "#636efa"]})

        return fig

    def create_user_map_box(self, df, lat, lng, apptheme="dark"):
        """
        `df `: datframe containing lattitude ,longitude information 
        `lat` : Name of the latittude column
        `lng` :Name of the longitude column
        """
        print("create_user_map_box", apptheme)
        bnd_box = {"min_lat": 8.4, "min_long": 68.7,
                   "max_lat": 37.67, "max_long": 97.25}
        lat = "latitude"
        lng = "longitude"
        # df transformation
        df["latitude"] = df.loc[df["latitude"] !=
                                "unknown", "latitude"].astype(np.float64)
        df["longitude"] = df.loc[df["longitude"] !=
                                 "unknown", "longitude"].astype(np.float64)
        df2 = df.query(f'{lat} > {bnd_box["min_lat"]}').query(f'{lat} <{bnd_box["max_lat"]}').query(
            f'{lng}>{bnd_box["min_long"]}').query(f'{lng}<{bnd_box["max_long"]}')
        df3 = df2.sort_values([lat, lng])

        df3.loc[:, "longitude_3857"], df3.loc[:, "latitude_3857"] = ds.utils.lnglat_to_meters(
            df3["longitude"], df3["latitude"])

        RESOLUTION = 1000
        cvs = ds.Canvas(plot_width=RESOLUTION, plot_height=RESOLUTION)
        agg = cvs.points(df3, x="longitude_3857", y="latitude_3857")
        color_map = colorcet.CET_C3
        if apptheme == "dark":
            color_map = colorcet.fire

        img = ds.tf.shade(agg, cmap=color_map).to_pil()

        coords_lat, coords_lon = agg.coords['latitude_3857'].values, agg.coords['longitude_3857'].values
        coordinates = [[coords_lon[0], coords_lat[0]],
                       [coords_lon[-1], coords_lat[0]],
                       [coords_lon[-1], coords_lat[-1]],
                       [coords_lon[0], coords_lat[-1]]]
        print(coordinates)
        t3857_to_4326 = Transformer.from_crs(3857, 4326, always_xy=True)
        values = [
            t3857_to_4326.transform(
                agg.coords["longitude_3857"].values[a],
                agg.coords["latitude_3857"].values[b],
            )
            for a, b in [(0, -1), (-1, -1), (-1, 0), (0, 0)]]
        print(values)
        fig = px.scatter_mapbox(
            df3[:1], lat='latitude', lon='longitude', zoom=2)
        # Add the datashader image as a mapbox layer image
        fig.update_layout(mapbox_style="open-street-map",
                          mapbox_layers=[
                              {
                                  "sourcetype": "image",
                                  "source": img,
                                  "coordinates": values
                              }],
                          margin={"l": 1, "r": 1, "t": 1, "r": 1, "b": 1}
                          )
        bounds_dict = dict(
            north=bnd_box["max_lat"],  # Maximum latitude
            south=bnd_box["min_lat"],  # Minimum latitude
            east=bnd_box["max_long"],  # Maximum longitude
            west=bnd_box["min_long"]   # Minimum longitude
        )
        fig.update_mapboxes(bounds=bounds_dict)

        return fig

    def create_language_trend(self, trend_type="likes",apptheme="dark"):
        date_format = '%Y-%m-%d'
        parent_kids_df = self.parent_kids_df
        video_likes = pd.read_csv("video_likes.csv")
        video_likes_kids = video_likes.merge(parent_kids_df.rename(columns={"id": "kid_id"})[["kid_id", "age_on_today"]],
                                             on="kid_id", how="left").dropna()
        parent_kids_df["dob"] = pd.to_datetime(
            parent_kids_df.age, format=date_format)
        parent_kids_df["age_on_today"] = parent_kids_df.dob.apply(
            get_age_per_today)

        stories = get_clean_stories('stories.csv')
        comments = get_comments_cleaned('comments.csv')
        categories = get_clean_categories("category.csv")
        stories2 = map_category_id_with_categories(stories, categories)

        langs = pd.read_csv("language.csv")
        langs = langs[langs["deleted_at"].isnull()]
        language_ids = langs["id"].tolist()
        lang_codes = langs["name"].to_list()
        lang_id_codes = dict(zip(language_ids, lang_codes))

        comments_on_stories = comments.merge(stories.rename(
            columns={"id": "story_id"}), on="story_id", how="left")
        comment_with_story_and_kid_age = comments_on_stories.rename(columns={"user_id": "kid_id"}).merge(
            parent_kids_df.rename(columns={"id": "kid_id"})[["kid_id", "age_on_today"]], on="kid_id", how="left")
        comment_withoutna = comment_with_story_and_kid_age.dropna()
        comment_withoutna["updated_date"] = pd.to_datetime(
            comment_withoutna["updated_at"])
        lang_trend1 = comment_withoutna.loc[:, [
            "updated_date", "age_on_today", "language"]]
        lang_trend1["updated_month"] = lang_trend1["updated_date"].apply(
            lambda date: date.strftime("%Y-%m"))
        # trends on comments
        lang_trend2 = lang_trend1.groupby(
            ["updated_month", "language"]).agg(
                {"language": "count"}).rename(columns={"language": "count"}).reset_index()

        video_likes_kids["updated_date"] = pd.to_datetime(
            video_likes_kids["updated_at"]).dt.date
        video_likes_kids["updated_month"] = video_likes_kids["updated_date"].apply(
            lambda date: date.strftime("%Y-%m"))
        like_lang_trend = video_likes_kids.merge(stories[["id", "language"]].rename(
            columns={"id": "video_id"}), on="video_id")[["updated_month", "language"]]

        like_lang_trend = like_lang_trend.groupby(["updated_month", "language"]).agg(
            {"language": "count"}).rename(columns={"language": "count"}).reset_index()

        lang_df = pd.read_csv('language.csv')
        lang_df = lang_df.loc[lang_df["deleted_at"].isna()]
        lang_mapper = get_lang_mapper(lang_df)
        lang_trend2["lang_str"] = lang_trend2["language"].apply(
            get_lang_id, args=(lang_mapper,))
        like_lang_trend["lang_str"] = like_lang_trend["language"].apply(
            get_lang_id, args=(lang_mapper,))
        language_colors = ["#3498db", "#e74c3c",
                           "#2ecc71", "#f39c12", "#e67e22"]
        figure_df = like_lang_trend if trend_type == "likes"  else lang_trend2
        fig = px.line(figure_df, x="updated_month", y="count", color="lang_str",
                      labels={'lang_str': 'Languages',
                              "count": "Comment count" if trend_type != "likes" else "Likes count", "updated_month": "Month"},
                      color_discrete_sequence=language_colors)
        
        fig.update_layout(
            {"template": "plotly_dark" if apptheme == 'dark' else "plotly_white"})
        return fig
