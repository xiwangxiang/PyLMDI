#use this for testing

#%%
#testing


# driver_input_data = pd.DataFrame(np.array([[100, 120], ['B', 100, 120]]), columns=['2000', '2001'], index=['A', 'B']) #test data from printed notes
# energy = pd.DataFrame(np.array([[60, 120], [40, 27]]), columns=['2000', '2001'], index=['A', 'B'])#test data from printed notes

#lets make the data much smaller first
activity_wide_small = activity_wide.iloc[:2, :4]
energy_wide_small = energy_wide.iloc[:2, :4]

driver_input_data = activity_wide_small
energy = energy_wide_small
