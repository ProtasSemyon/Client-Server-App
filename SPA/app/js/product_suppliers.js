const productSuppliersButton = document.querySelector('#product_suppliers');
tableContainer = document.querySelector('#table-container');
const productSuppliersUrl = '/api/product_suppliers'

function clearHtml() {
  tableContainer.innerHTML = '';
}

function addRow_productSuppliers(item, tableBody, productsArr, suppliersArr) {
  let product = item["Products"]
  let supplier = item["Suppliers"]
  let product_supplier = item["ProductSuppliers"]
  const row = document.createElement('tr');
  const idCell = document.createElement('td');
  idCell.textContent = product_supplier.product_supplier_id;
  const productIdCell = document.createElement('td');
  const supplierIdCell = document.createElement('td');

  const updateButtonCell = document.createElement('td');
  const updateButton = document.createElement('button');
  updateButton.textContent = 'Update';

  const deleteButtonCell = document.createElement('td');
  const deleteButton = document.createElement('button');
  deleteButton.textContent = 'Delete';

  const productIdSelect = document.createElement('select')
  const firstProductOp = document.createElement('option')
  firstProductOp.setAttribute('value', product.product_id);
  firstProductOp.setAttribute('selected', '');
  firstProductOp.setAttribute('hidden', '');
  firstProductOp.textContent = product.product_name
  productIdSelect.appendChild(firstProductOp);
  productsArr.forEach(item => {
    let op = document.createElement('option')
    op.setAttribute('value', item.product_id)
    op.textContent = item.product_name
    productIdSelect.appendChild(op)
  });

  const supplierIdSelect = document.createElement('select')
  const firstSupplierOp = document.createElement('option')
  firstSupplierOp.setAttribute('value', supplier.supplier_id);
  firstSupplierOp.setAttribute('selected', '');
  firstSupplierOp.setAttribute('hidden', '');
  firstSupplierOp.textContent = supplier.supplier_name
  supplierIdSelect.appendChild(firstSupplierOp);
  suppliersArr.forEach(item => {
    let op = document.createElement('option')
    op.setAttribute('value', item.supplier_id)
    op.textContent = item.supplier_name
    supplierIdSelect.appendChild(op)
  });

  productIdCell.appendChild(productIdSelect);
  supplierIdCell.appendChild(supplierIdSelect);

  updateButton.addEventListener('click', () => {
    const jwt_token = localStorage.getItem('jwt_token');

    const dataForAdd = {
      product_id: productIdSelect.value, 
      supplier_id: supplierIdSelect.value, 
    };

    fetch(productSuppliersUrl + '/' + idCell.textContent, {
      method: 'PUT',
      body: JSON.stringify(dataForAdd),
      headers: {
        'Content-Type': 'application/json',
        'Authorization' :'Bearer '+ jwt_token
      }
    })
    .then(response => {
      if (response.ok) {
        console.log('Данные успешно обновлены');
      } else {
        console.error('Произошла ошибка при обновлении данных');
      }
      return response.json()
    }).then(data => {
      fillTableContainer_productSuppliers(data);
    })
    .catch(error => {
      console.error('Произошла ошибка при отправке запроса на сервер', error);
    });
  })

  deleteButton.addEventListener('click', () => {
    const jwt_token = localStorage.getItem('jwt_token');

    fetch(productSuppliersUrl + '/' + idCell.textContent, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Authorization' :'Bearer '+ jwt_token
      }
    })
    .then(response => {
      if (response.ok) {
        console.log('Данные успешно обновлены');
      } else {
        console.error('Произошла ошибка при обновлении данных');
      }
      return response.json()
    }).then(data => {
      fillTableContainer_productSuppliers(data);
    })
    .catch(error => {
      console.error('Произошла ошибка при отправке запроса на сервер', error);
    });
  })
  
  updateButtonCell.appendChild(updateButton);
  deleteButtonCell.appendChild(deleteButton);

  row.appendChild(idCell);
  row.appendChild(productIdCell)
  row.appendChild(supplierIdCell)
  row.appendChild(updateButtonCell)
  row.appendChild(deleteButtonCell)

  tableBody.appendChild(row);
}

function addButton_productSuppliers(tableBody, productsArr, suppliersArr) {
  const row = document.createElement('tr');
  const idCell = document.createElement('td');
  const productIdCell = document.createElement('td');
  const supplierIdCell = document.createElement('td');

  const addButtonCell = document.createElement('td');
  const addButton = document.createElement('button');
  addButton.textContent = 'Add';

  const productIdSelect = document.createElement('select')
  const firsProductOp = document.createElement('option')
  firsProductOp.setAttribute('value', '');
  firsProductOp.setAttribute('selected', '');
  firsProductOp.setAttribute('hidden', '');
  firsProductOp.textContent = "Choose a product"
  productIdSelect.appendChild(firsProductOp);
  productsArr.forEach(item => {
    let op = document.createElement('option')
    op.setAttribute('value', item.product_id)
    op.textContent = item.product_name
    productIdSelect.appendChild(op)
  });

  const supplierIdSelect = document.createElement('select')
  const firstSupplierOp = document.createElement('option')
  firstSupplierOp.setAttribute('selected', '');
  firstSupplierOp.setAttribute('hidden', '');
  firstSupplierOp.textContent = "Choose a supplier"
  supplierIdSelect.appendChild(firstSupplierOp);
  suppliersArr.forEach(item => {
    let op = document.createElement('option')
    op.setAttribute('value', item.supplier_id)
    op.textContent = item.supplier_name
    supplierIdSelect.appendChild(op)
  });

  productIdCell.appendChild(productIdSelect);
  supplierIdCell.appendChild(supplierIdSelect);

  addButton.addEventListener('click', () => {
    const jwt_token = localStorage.getItem('jwt_token');

    const dataForAdd = {
      product_id: productIdSelect.value, 
      supplier_id: supplierIdSelect.value, 
    };

    fetch(productSuppliersUrl, {
      method: 'PUT',
      body: JSON.stringify(dataForAdd),
      headers: {
        'Content-Type': 'application/json',
        'Authorization' :'Bearer '+ jwt_token
      }
    })
    .then(response => {
      if (response.ok) {
        console.log('Данные успешно обновлены');
      } else {
        console.error('Произошла ошибка при обновлении данных');
      }
      return response.json()
    }).then(data => {
      console.log(data);
      fillTableContainer_productSuppliers(data);
    })
    .catch(error => {
      console.error('Произошла ошибка при отправке запроса на сервер', error);
    });
  });

  addButtonCell.appendChild(addButton);

  row.appendChild(idCell);
  row.appendChild(productIdCell)
  row.appendChild(supplierIdCell)
  row.appendChild(addButtonCell)
  tableBody.appendChild(row);
}

function fillTableContainer_productSuppliers(data) {
  clearHtml()
  tableContainer.innerHTML = `
    <table>
      <thead>
        <tr>
          <th></th>
          <th>Product name</th>
          <th>Supplier name</th>
        </tr>
      </thead>
      <tbody>
      </tbody>
    </table>
      `
  let arr = data["product_suppliers"];
  let productsArr = data["products"];
  let suppliersArr = data["suppliers"];
  const tableBody = tableContainer.querySelector('tbody');

  arr.forEach(item => addRow_productSuppliers(item, tableBody, productsArr, suppliersArr));
  addButton_productSuppliers(tableBody, productsArr, suppliersArr);
}

productSuppliersButton.addEventListener('click', () => {
  fetch(productSuppliersUrl)
    .then(response => response.json())
    .then(data => {
      console.log(data);
      fillTableContainer_productSuppliers(data);
})});