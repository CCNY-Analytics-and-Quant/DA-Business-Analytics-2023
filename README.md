# Mamma Mia's
### Mama Mia Group met through Zoom and Discord to discuss ideas and apply the analytical process to the following question: 
### “I am looking to open a pizza restaurant, what suggestions do you have for success?”
### This question was reframed to, what opportunities do you have to maximize profit? From there we figured out what information we needed to identify this opportunity. We extracted our information from the “sum_23” pizza database, as well as information from CNY Weather. We then created and discussed data that was important for us to use, we discussed joins and worked with SQL to join tables together. With the data, we created a couple of tables and discussed the trends and relationships of the data. Lastly, we built a presentation for the CEO that tells a story. 


## Graph #1a: Heatmap: Hours and quantities, filtered by day
## Graph #1b: Treemap: Sorts by best days then best hours
## Graph #2: Subplot: Rain and orders relationship
## Graph #3: Histogram: Pizza categories/types
## Graph #4: Histogram: Ingrediants filtered by how often they are grouped
## Graph #5a: Pie Chart: The greek pizza orders measured by size
## Graph #5ab: Bar plot: The orders measured by size, excluding XL,XXL, brie_carre, big_meats, and five_cheese.
	


### Graph #1a: Heatmap: Hours and quantities, filtered by day
This graph was used to provide a visualization of the general peak hours on a day to day basis. In this data there is a clear trend during the weekday, where the orders peak in the early afternoon. Whereas on the weekend the orders are not concentrated early in the afternoon, they are dispersed to the entirety of the day. It is recommended that the restuarant schedules in this format:

Monday - Friday: 60% staff early day / 40% staff late evening
Saturday - Sunday: 50% staff early day / 50% staff late evening


### Graph #1b: Treemap: Sorts by best days then best hours
The treemap shows exactly which days has the highest concentration of orders. We recommend that the restuarant has its highest quantity of workers on the days its busiest. And has its lowest quantity of workers on the days it is least busy.



### Graph #2: Subplot: Rain and orders relationship
The weather and orders relationship gives an accurate prediction on how orders are expected to be. The restuarnat needs to use a weather forecast that will allow them to understand their estimated order count in the future time. Like a crystal ball. Then manange scheduling during these times so the least amount of workers work in the season with heavy weather conditions, and most amount of workers in peak seasons. Also limit ingredients purchased in bulk during heavy weather seasons, and buy extra in peak season.

### Graph #3: Histogram: Pizza categories/types
Each category is filtered by color which shows the pizza types per the category, as well a visualization of which pizzas sell the most. Classic is the best option, but chicken is good aswell pound for pound. We advise the restuarant to increase chicken options because individial for individual pizza type, chicken is just as good as classic, but has the least amount of pizza types across all categories. 

### Graph #4: Histogram: Ingrediants filtered by how often they are grouped
The ingredients are displayed seperately so that the restuarant has a report of how often each ingredient is used in their orders. The restuarant needs to make sure to buy a large quantity in ingredients for those that are stacked the highest on the histogram. Similary they need to place a limit on how many ingredients to buy, especially for the 'unique' ingredients that are not used very often.


### Graph #5a: Pie Chart: The greek pizza orders measured by size
Since the greek pizza is the only pizza that comes in XL and XXL. It is the only option we have when determining how viable XL and XXL are as pizza size options. The data concludes that XXL is not worth including in the menu because of how poor it sells. Where XL shows strong expectations due to how often it was ordered in this one pizza type. 


### Graph #5ab: Bar plot: The orders measured by size, excluding XL,XXL, brie_carre, big_meats, and five_cheese.
The pizzas that only come in one size such as big_meats ( only in small ) are excluded from the data. We wanted to see how favorable each size is. Because those only come in one option it would not provide meaningful insight to the data. The trend is that as size increases so does orders. The resturant should make every pizza in classic and chicken come in Small, Medium, Large and XLarge. The supreme and veggie should come in Small, Medium, and Large only because we dont think the demand for these pizzas are high enough to consider adding an extra size.

