from shiny import render, ui, reactive
from shiny.express import input
import pandas as pd
import seaborn as sns
import random

# Define a dictionary of options and corresponding representations
diceDictLabel = {"4":"d4","6":"d6","8":"d8","10":"d10","12":"d12","20":"d20"}
diceDictNum = {"4":4,"6":6,"8":8,"10":10,"12":12,"20":20}
results = []


# Create title
ui.panel_title("Dice Roller")

with ui.layout_column_wrap():
    # Create an array of horizontally aligned radio buttons
    # Allow user to select the type of dice to be rolled
    ui.input_radio_buttons(
        "dice",
        "Select your dice",
        diceDictLabel,
        inline=True
    )
    
    # Determine the number of dice to be rolled
    ui.input_numeric(
        "dN",
        "How many?",
        value=1,
        min=1,
        max=256
    )

# Verbose Output: Confirm the user's selection
@render.text
def txt():
    return f"You selected {input.dN()}{diceDictLabel[input.dice()]}"

# Determine if the user wants a history of rolls
ui.input_checkbox("history","Show Roll History?", False)
# @render.ui
def value():
    return input.history()

# Give the user a fun lil button
ui.input_action_button("roll","Roll!")
# Output the result
@render.text()
@reactive.event(input.roll)
def roller():
    val = 0
    if not input.history():
        print("Clearing history")
        results.clear()
    for i in range(input.dN()):
        val += random.randint(1,int(input.dice()))
        i=i+1
    results.append(val)
    print("Results", results)
    return f"Rolled {results}"


ui.input_action_button("plot","Plot Results")
    # Output a time series of results
    
with ui.layout_column_wrap():
    @render.plot(alt="A seaborn timeseries of results")
    @reactive.event(input.plot)
    def plot():
        rollList = range(1,len(results)+1)
        df= pd.DataFrame(list(zip(rollList,results)),columns=["Roll #","Result"])
        print(rollList)
        ax = sns.lineplot(x="Roll #", y="Result",data=df).set(title="Roll History")
        return ax

    @render.plot(alt="A histogram of results")
    @reactive.event(input.plot)
    def plot2():
        df=pd.DataFrame(results)
        ax=sns.histplot(df)
        return ax
    

# Further Ideas: Run a Chi-Squared test and ouput the p-value for a goodness of fit to a uniform distribution?

