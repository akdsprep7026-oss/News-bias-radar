import plotly.graph_objects as go
import pandas as pd

def create_sentiment_chart(sentiment_data):
    """
    Creates a more polished, gauge-like sentiment chart using Plotly.
    """
    label = sentiment_data['label']
    score = sentiment_data['score']
    
    # Define color and text based on sentiment
    if label == 'NEGATIVE':
        color = "#D9534F" # Red
        text = f"Negative ({score:.2%})"
    elif label == 'POSITIVE':
        color = "#5CB85C" # Green
        text = f"Positive ({score:.2%})"
    else:
        color = "#0077B6" # Blue
        text = f"Neutral ({score:.2%})"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "Sentiment"},
        number={'font': {'size': 36}},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 1], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 0.5], 'color': 'rgba(217, 83, 79, 0.2)'},
                {'range': [0.5, 1], 'color': 'rgba(92, 184, 92, 0.2)'}
            ],
        }
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20))
    return fig


def create_bias_chart(bias_data):
    """
    Creates a more polished bar chart for political bias, handling the zero-score case.
    """
    # If both scores are 0, we don't need a chart. Return None.
    if bias_data['left_leaning_score'] == 0 and bias_data['right_leaning_score'] == 0:
        return None

    # Create a DataFrame from the bias data
    df = pd.DataFrame([
        {'Leaning': 'Left-Leaning', 'Count': bias_data['left_leaning_score']},
        {'Leaning': 'Right-Leaning', 'Count': bias_data['right_leaning_score']}
    ])
    
    color_map = {'Left-Leaning': '#0077B6', 'Right-Leaning': '#D9534F'}

    fig = go.Figure()
    
    for leaning, color in color_map.items():
        sub_df = df[df['Leaning'] == leaning]
        fig.add_trace(go.Bar(
            x=sub_df['Count'],
            y=sub_df['Leaning'],
            orientation='h',
            name=leaning,
            marker_color=color,
            text=sub_df['Count'],
            textposition='auto'
        ))

    fig.update_layout(
        title_text='Political Bias Word Count',
        xaxis_title='Word Count',
        yaxis_title='',
        barmode='stack',
        showlegend=False,
        height=250,
        margin=dict(l=20, r=20, t=40, b=20),
        yaxis=dict(showticklabels=False) 
    )
    return fig