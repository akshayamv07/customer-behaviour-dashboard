import plotly.express as px
import plotly.graph_objects as go


def line_chart(df, x, y, title):
    fig = px.line(
        df,
        x=x,
        y=y,
        markers=True,
        title=title
    )

    fig.update_layout(
        template="plotly_white",
        hovermode="x unified"
    )

    return fig


def bar_chart(df, x, y, title, color=None, text=None):

    fig = px.bar(
        df,
        x=x,
        y=y,
        color=color,
        text=text,
        title=title
    )

    fig.update_layout(
        template="plotly_white"
    )

    return fig


def pie_chart(df, names, title):

    fig = px.pie(
        df,
        names=names,
        title=title,
        hole=0.45
    )

    fig.update_layout(
        template="plotly_white"
    )

    return fig


def scatter_chart(
    df,
    x,
    y,
    color,
    size=None,
    hover=None,
    title=""
):

    kwargs = {
        "data_frame": df,
        "x": x,
        "y": y,
        "color": color,
        "title": title
    }

    if size and size in df.columns:
        kwargs["size"] = size

    if hover and hover in df.columns:
        kwargs["hover_name"] = hover

    fig = px.scatter(**kwargs)

    fig.update_layout(
        template="plotly_white"
    )

    return fig


def histogram(df, x, color=None, title=""):

    fig = px.histogram(
        df,
        x=x,
        color=color,
        title=title
    )

    fig.update_layout(
        template="plotly_white"
    )

    return fig


def box_plot(df, x, y, color=None, title=""):

    fig = px.box(
        df,
        x=x,
        y=y,
        color=color,
        title=title
    )

    fig.update_layout(
        template="plotly_white"
    )

    return fig


def funnel_chart(df):

    fig = go.Figure(
        go.Funnel(
            y=df["Stage"],
            x=df["Customers"]
        )
    )

    fig.update_layout(
        title="Purchase Funnel",
        template="plotly_white"
    )

    return fig