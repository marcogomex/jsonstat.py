
Notebook: using jsonstat.py python library with jsonstat format version 1.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This Jupyter notebook shows the python library
`jsonstat.py <http://github.com/26fe/jsonstat.py>`__ in action. The
`JSON-stat <https://json-stat.org/>`__ is a simple lightweight JSON
dissemination format. For more information about the format see the
`official site <https://json-stat.org/>`__. This example shows how to
explore the example data file
`oecd-canada <http://json-stat.org/samples/oecd-canada.json>`__ from
json-stat.org site. This file is complaint to the version 1 of jsonstat.

.. code:: python

    # all import here
    from __future__ import print_function
    import os
    import pandas as ps # using panda to convert jsonstat dataset to pandas dataframe
    import jsonstat     # import jsonstat.py package
    
    import matplotlib as plt  # for plotting 


.. parsed-literal::

    The history saving thread hit an unexpected error (DatabaseError('database disk image is malformed',)).History will not be written to the database.


.. code:: python

    %matplotlib inline

Download or use cached file oecd-canada.json. Caching file on disk
permits to work off-line and to speed up the exloration of the data.

.. code:: python

    url = 'http://json-stat.org/samples/oecd-canada.json'
    file_name = "oecd-canada.json"
    
    file_path = os.path.abspath(os.path.join("..", "tests", "fixtures", "json-stat.org", file_name))
    if os.path.exists(file_path):
        print("using already downloaded file {}".format(file_path))
    else:
        print("download file and storing on disk")
        jsonstat.download(url, file_name)
        file_path = file_name


.. parsed-literal::

    download file and storing on disk


Initialize JsonStatCollection from the file and print the list of
dataset contained into the collection.

.. code:: python

    collection = jsonstat.from_file(file_path)
    collection




.. parsed-literal::

    0: dataset 'oecd'
    1: dataset 'canada'



Select the dataset named ``oedc``. Oecd dataset has three dimensions
(concept, area, year), and contains 432 values.

.. code:: python

    oecd = collection.dataset('oecd')
    oecd




.. parsed-literal::

    name:   'oecd'
    label:  'Unemployment rate in the OECD countries 2003-2014'
    source: 'Unemployment rate in the OECD countries 2003-2014'
    size: 432
    3 dimensions:
      0: dim id: 'concept' label: 'indicator' size: '1' role: 'metric'
      1: dim id: 'area' label: 'OECD countries, EU15 and total' size: '36' role: 'geo'
      2: dim id: 'year' label: '2003-2014' size: '12' role: 'time'



Shows some detailed info about dimensions

.. code:: python

    for d in oecd.dimensions():
        print("*** info for dimensions '{}'".format(d.name()))
        d.info()


.. parsed-literal::

    *** info for dimensions 'concept'
    index
      pos idx      label   
        0 'UNR'    'unemployment rate'
    
    *** info for dimensions 'area'
    index
      pos idx      label   
        0 'AU'     'Australia'
        1 'AT'     'Austria'
        2 'BE'     'Belgium'
        3 'CA'     'Canada'
        4 'CL'     'Chile' 
        5 'CZ'     'Czech Republic'
        6 'DK'     'Denmark'
        7 'EE'     'Estonia'
        8 'FI'     'Finland'
        9 'FR'     'France'
       10 'DE'     'Germany'
       11 'GR'     'Greece'
       12 'HU'     'Hungary'
       13 'IS'     'Iceland'
       14 'IE'     'Ireland'
       15 'IL'     'Israel'
       16 'IT'     'Italy' 
       17 'JP'     'Japan' 
       18 'KR'     'Korea' 
       19 'LU'     'Luxembourg'
       20 'MX'     'Mexico'
       21 'NL'     'Netherlands'
       22 'NZ'     'New Zealand'
       23 'NO'     'Norway'
       24 'PL'     'Poland'
       25 'PT'     'Portugal'
       26 'SK'     'Slovak Republic'
       27 'SI'     'Slovenia'
       28 'ES'     'Spain' 
       29 'SE'     'Sweden'
       30 'CH'     'Switzerland'
       31 'TR'     'Turkey'
       32 'UK'     'United Kingdom'
       33 'US'     'United States'
       34 'EU15'   'Euro area (15 countries)'
       35 'OECD'   'total' 
    
    *** info for dimensions 'year'
    index
      pos idx      label   
        0 '2003'   ''      
        1 '2004'   ''      
        2 '2005'   ''      
        3 '2006'   ''      
        4 '2007'   ''      
        5 '2008'   ''      
        6 '2009'   ''      
        7 '2010'   ''      
        8 '2011'   ''      
        9 '2012'   ''      
       10 '2013'   ''      
       11 '2014'   ''      
    


Accessing value in the dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Print the value in oecd dataset for area = IT and year = 2012

.. code:: python

    oecd.value(area='IT', year='2012')




.. parsed-literal::

    10.55546863



.. code:: python

    oecd.value(concept='unemployment rate',area='Australia',year='2004') # 5.39663128




.. parsed-literal::

    5.39663128



.. code:: python

    oecd.value(concept='UNR',area='AU',year='2004')




.. parsed-literal::

    5.39663128



Trasforming dataset into pandas DataFrame
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    df_oecd = oecd.to_data_frame('year', content='id')
    df_oecd.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>concept</th>
          <th>area</th>
          <th>Value</th>
        </tr>
        <tr>
          <th>year</th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>2003</th>
          <td>UNR</td>
          <td>AU</td>
          <td>5.943826</td>
        </tr>
        <tr>
          <th>2004</th>
          <td>UNR</td>
          <td>AU</td>
          <td>5.396631</td>
        </tr>
        <tr>
          <th>2005</th>
          <td>UNR</td>
          <td>AU</td>
          <td>5.044791</td>
        </tr>
        <tr>
          <th>2006</th>
          <td>UNR</td>
          <td>AU</td>
          <td>4.789363</td>
        </tr>
        <tr>
          <th>2007</th>
          <td>UNR</td>
          <td>AU</td>
          <td>4.379649</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    df_oecd['area'].describe() # area contains 36 values




.. parsed-literal::

    count     432
    unique     36
    top        IS
    freq       12
    Name: area, dtype: object



Extract a subset of data in a pandas dataframe from the jsonstat
dataset. We can trasform dataset freezing the dimension area to a
specific country (Canada)

.. code:: python

    df_oecd_ca = oecd.to_data_frame('year', content='id', blocked_dims={'area':'CA'})
    df_oecd_ca.tail()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>concept</th>
          <th>area</th>
          <th>Value</th>
        </tr>
        <tr>
          <th>year</th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>2010</th>
          <td>UNR</td>
          <td>CA</td>
          <td>7.988900</td>
        </tr>
        <tr>
          <th>2011</th>
          <td>UNR</td>
          <td>CA</td>
          <td>7.453610</td>
        </tr>
        <tr>
          <th>2012</th>
          <td>UNR</td>
          <td>CA</td>
          <td>7.323584</td>
        </tr>
        <tr>
          <th>2013</th>
          <td>UNR</td>
          <td>CA</td>
          <td>7.169742</td>
        </tr>
        <tr>
          <th>2014</th>
          <td>UNR</td>
          <td>CA</td>
          <td>6.881227</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    df_oecd_ca['area'].describe()  # area contains only one value (CA)




.. parsed-literal::

    count     12
    unique     1
    top       CA
    freq      12
    Name: area, dtype: object



.. code:: python

    df_oecd_ca.plot(grid=True)




.. parsed-literal::

    <matplotlib.axes._subplots.AxesSubplot at 0x1136dc6a0>




.. image:: oecd-canada-jsonstat_v1_files/oecd-canada-jsonstat_v1_21_1.png


Trasforming a dataset into a python list
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    oecd.to_table()[:5]




.. parsed-literal::

    [['indicator', 'OECD countries, EU15 and total', '2003-2014', 'Value'],
     ['unemployment rate', 'Australia', '2003', 5.943826289],
     ['unemployment rate', 'Australia', '2004', 5.39663128],
     ['unemployment rate', 'Australia', '2005', 5.044790587],
     ['unemployment rate', 'Australia', '2006', 4.789362794]]



It is possible to trasform jsonstat data into table in different order

.. code:: python

    order = [i.name() for i in oecd.dimensions()]
    order = order[::-1]  # reverse list
    order = oecd.from_vec_idx_to_vec_dim(order)
    table = oecd.to_table(order=order)
    table[:5]




.. parsed-literal::

    [['indicator', 'OECD countries, EU15 and total', '2003-2014', 'Value'],
     ['unemployment rate', 'Australia', '2003', 5.943826289],
     ['unemployment rate', 'Austria', '2003', 4.278559338],
     ['unemployment rate', 'Belgium', '2003', 8.158333333],
     ['unemployment rate', 'Canada', '2003', 7.594616751]]

