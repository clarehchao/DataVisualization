# Data Visualization of Parents and Teens Survey Data from [Pulse](https://www.pulsepeers.com/)

[Pulse](https://www.pulsepeers.com/) is a start-up company building solutions to support Teens' mental health. This is an exploratory data analysis that observed trends in survey data among different demographics. Data visualization dashboards were designed and created to facilitate the analysis using [Plotly Dash](https://dash.plotly.com/).

### Data cleaning and wrangling
- Since the survey data were all text and were recorded from multiple surveys with different format, data were cleaned and standardized with following in mind:
  - Count the number of Teens in the family and compute Median age of the teens in each family entry
  - Since multiple-choice survey questions had no priority in order of entry, One-Hot Encoding was used to creates binary columns indicating the presence or absence of each category for each survey response for ease of further data analysis and queries.

### Data Visualization
- [An interactive dashboard with multiple navigation links](https://clarechao.pythonanywhere.com/) using *dash-boostrap-component* was designed and created using [Plotly Dash](https://dash.plotly.com/)
  - Interactive vertical bar chart was created to visualize what parents are concerned about with drop-down menu of demographic options
  - Another vertical bar chart was created with live-updated view of what source of advice parents who are concerned about a particular category seek 


### More ideas/thoughts to explore
- Create more visualization to explore other survey data specifically social medial use and what teens are struggling with
- For survey data that users wrote their thoughts, not multiple-choice questions, apply sentiment analysis or explore other language-related analysis to pull out thoughts, ideas, and emotions.
