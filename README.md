# 10X_genomics_data_tool
Script that extracts the cell boundaries of a Xenium Prime dataset and transforms them into cells (128x128 TIFF). Loads the data into a specified directory.

Here is an example of what the cell_boundaries DataFrame looks like:
<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>cell_id</th>
      <th>vertex_x</th>
      <th>vertex_y</th>
      <th>label_id</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>aaaadnje-1</td>
      <td>445.61252</td>
      <td>1697.6626</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>aaaadnje-1</td>
      <td>444.76250</td>
      <td>1698.3000</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>aaaadnje-1</td>
      <td>443.06250</td>
      <td>1698.3000</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>aaaadnje-1</td>
      <td>442.00000</td>
      <td>1699.3625</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>aaaadnje-1</td>
      <td>442.63750</td>
      <td>1700.2125</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>

Each cell has boundary points that define its border. For higher cell quality, I have chosen to process ONLY the cells with 25 boundary points (as opposed to some smaller number). This change means that around one percent of the data is excluded (from what I've seen with the human pancreas and human prostate data).

This is an example of what the cells might look like:

![image](https://github.com/user-attachments/assets/ffd98ac5-d125-455c-bf18-1e7a00fb2065)

Here is an example of the processed cell:

![image](https://github.com/user-attachments/assets/58abfda6-eec0-4dbb-b81e-a6a5af8ebbd5)

It has been rotated in a standardizing process. 




