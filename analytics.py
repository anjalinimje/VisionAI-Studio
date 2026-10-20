import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go

def object_bar_chart(object_counts, chart_key=None):
    if not object_counts:
        return go.Figure()
    
    df = pd.DataFrame(
        {
            "Object": list(object_counts.keys()),
            "Count": list(object_counts.values())
        }
    )

    fig = px.bar(
        df,
        x="Object",
        y="Count",
        color="Count",
        text="Count",
        title="Detected Object Distribution"
    )

    fig.update_layout(
        height=450,
        template="plotly_dark",
        title_x=0.5,
        xaxis_title="Detected Objects",
        yaxis_title="Count",
        font=dict(size=14)
    )

    fig.update_layout(
        paper_bgcolor="rgba(8, 13, 31, 0)",
        plot_bgcolor="rgba(21, 27, 53, 0.85)",
        font=dict(
            family="Arial, sans-serif",
            color="#E2E8FF",
            size=13
        ),
        title_font=dict(
            color="#C4B5FD",
            size=17
        ),
        legend=dict(
            font=dict(color="#E2E8FF"),
            bgcolor="rgba(21, 27, 53, 0)"
        ),
        margin=dict(l=35, r=25, t=65, b=45)
    )

    fig.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key=chart_key
    )

def object_pie_chart(object_counts, chart_key=None):
        if not object_counts:
            return go.Figure()
        
        df = pd.DataFrame(
            {
                "Object": list(object_counts.keys()),
                "Count": list(object_counts.values())
            }
        )

        fig = px.pie(
            df,
            names="Object",
            values="Count",
            title="Object Class Distribution",
            hole=0.45
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        fig.update_layout(
            height=500,
            title_x=0.5,
            template="plotly_dark",
            legend_title="Objects"
        )

        fig.update_layout(
            paper_bgcolor="rgba(8, 13, 31, 0)",
            plot_bgcolor="rgba(21, 27, 53, 0.85)",
            font=dict(
                family="Arial, sans-serif",
                color="#E2E8FF",
                size=13
            ),
            title_font=dict(
                color="#C4B5FD",
                size=17
            ),
            legend=dict(
                font=dict(color="#E2E8FF"),
                bgcolor="rgba(21, 27, 53, 0)"
            ),
            margin=dict(l=35, r=25, t=65, b=45)
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            key=chart_key
        )

def confidence_histogram(confidence_scores):
    if not confidence_scores:
        return go.Figure()
    
    df = pd.DataFrame({
        "Confidence": confidence_scores
    })

    fig = px.histogram(
        df,
        x="Confidence",
        nbins=10,
        title="Confidence Score Distribution"
    )

    fig.update_layout(
        height=420,
        template="plotly_dark",
        title_x=0.5,
        xaxis_title="Confidence Score",
        yaxis_title="Frequency"
    )


    fig.update_layout(
        paper_bgcolor="rgba(8, 13, 31, 0)",
        plot_bgcolor="rgba(21, 27, 53, 0.85)",
        font=dict(
            family="Arial, sans-serif",
            color="#E2E8FF",
            size=13
        ),
        title_font=dict(
            color="#C4B5FD",
            size=17
        ),
        legend=dict(
            font=dict(color="#E2E8FF"),
            bgcolor="rgba(21, 27, 53, 0)"
        ),
        margin=dict(l=35, r=25, t=65, b=45)
    )


    return fig


def confidence_gauge(confidence_scores):

    if confidence_scores:
        average_confidence = sum(confidence_scores) / len(confidence_scores)
    else:
        average_confidence = 0

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",

            value=average_confidence * 100,

            number={
                "suffix": "%",
                "font": {"size": 42}
            },

            title={
                "text": "Average Confidence",
                "font": {"size": 24}
            },

            gauge={

                "axis": {"range": [0, 100]},

                "bar": {
                    "color": "#A855F7"
                },

                "steps": [
                    {"range": [0, 40], "color": "#3B1D38"},
                    {"range": [40, 70], "color": "#30264D"},
                    {"range": [70, 100], "color": "#173B50"}
            ]
            }
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=350
        
    )


    fig.update_layout(
        paper_bgcolor="rgba(8, 13, 31, 0)",
        plot_bgcolor="rgba(21, 27, 53, 0.85)",
        font=dict(
            family="Arial, sans-serif",
            color="#E2E8FF",
            size=13
        ),
        title_font=dict(
            color="#C4B5FD",
            size=17
        ),
        legend=dict(
            font=dict(color="#E2E8FF"),
            bgcolor="rgba(21, 27, 53, 0)"
        ),
        margin=dict(l=35, r=25, t=65, b=45)
    )

    return fig