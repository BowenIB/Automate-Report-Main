from plugins.send_to_slack import send_to_slack
from plugins.transform.read_transform import append_all_files
import matplotlib.pyplot as plt 


file_bytes = "output/sales_per_month.png"

# analyze and create graph
data = append_all_files('/Users/Bowen/Downloads/Project_1/automate_report/data/sales_product_data/Sales_December_2019.csv')

# transform
data.drop (
    data[data["Quantity Ordered"] == "Quantity Ordered"].index, inplace=True)

data["total_price"] = data["Quantity Ordered"].astype(
    float) * data["Price Each"].astype(float) 

data_transformed = data.groupby('Product').agg({"total_price": "sum"}).reset_index().tail(3)

print(data_transformed)

fig, ax =plt.subplots(2)

ax[0].bar(data_transformed['Product'], data_transformed['total_price'])
ax[0].set_xlabel('Product')
ax[0].set_ylabel('Total Sales (USD)')

fig.savefig(file_bytes, bbox_inches='tight')

send_to_slack.execute('Ini adalah laporan hari ini', '#automate_report', file_bytes)

