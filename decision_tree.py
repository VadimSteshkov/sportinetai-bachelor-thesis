import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_graphviz
import graphviz
import pydotplus
from IPython.display import Image

# Load the dataset (ensure the file path is correct)
ufc_data_cleaned = pd.read_csv('data/processed/ufc_fight_data_cleaned.csv')

# Encode target variable: 1 for Red win, 0 for Blue win
ufc_data_cleaned['red_wins'] = (ufc_data_cleaned['winner'] == 'Red').astype(int)

# Define features and target variable
features = ['reach_diff', 'age_diff', 'sig_str_diff', 'td_acc_diff', 'total_rounds']
X = ufc_data_cleaned[features]
y = ufc_data_cleaned['red_wins']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Create an unpruned decision tree
clf = DecisionTreeClassifier(random_state=42)  # No constraints
clf.fit(X_train, y_train)

# Export the tree to Graphviz format
dot_data = export_graphviz(
    clf,
    out_file=None,
    feature_names=features,
    class_names=['Blue Win', 'Red Win'],
    filled=True,
    rounded=True,
    special_characters=True
)

# Convert to a graph and improve rendering settings
graph = pydotplus.graph_from_dot_data(dot_data)
graph.set_graph_defaults(fontsize='12', dpi='300')  # Set font size and DPI for better quality

# Save to file
graph.write_png("decision_tree_output_graphviz_high_quality.png")

# Display in Jupyter Notebook (optional)
Image(graph.create_png())
