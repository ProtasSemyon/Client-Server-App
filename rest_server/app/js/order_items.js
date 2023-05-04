const orderItemsButton = document.querySelector('#order_items');
tableContainer = document.querySelector('#table-container');
const orderItemsUrl = '/api/order_items'

function clearHtml() {
  tableContainer.innerHTML = '';
}

function addRow_orderItems(item, tableBody, ordersArr, productsArr) {
  let order = item["Orders"]
  let product = item["Products"]
  let order_product = item["OrderItems"]
  const row = document.createElement('tr');
  const idCell = document.createElement('td');
  idCell.textContent = order_product.order_item_id;
  const orderIdCell = document.createElement('td');
  const productIdCell = document.createElement('td');
  const quantityCell = document.createElement('td');
  const priceCell = document.createElement('td');

  const updateButtonCell = document.createElement('td');
  const updateButton = document.createElement('button');
  updateButton.textContent = 'Update';

  const deleteButtonCell = document.createElement('td');
  const deleteButton = document.createElement('button');
  deleteButton.textContent = 'Delete';

  const orderIdSelect = document.createElement('select')
  const firstOrderOp = document.createElement('option')
  firstOrderOp.setAttribute('value', order.order_id);
  firstOrderOp.setAttribute('selected', '');
  firstOrderOp.setAttribute('hidden', '');
  firstOrderOp.textContent = order.order_id
  orderIdSelect.appendChild(firstOrderOp);
  ordersArr.forEach(item => {
    let op = document.createElement('option')
    op.setAttribute('value', item.order_id)
    op.textContent = item.order_id
    orderIdSelect.appendChild(op)
  });

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

  const quantityInput = document.createElement('input')
  quantityInput.setAttribute('type', 'number')
  quantityInput.setAttribute('step', '1')
  quantityInput.setAttribute('value', order_product.quantity)

  const priceInput = document.createElement('input')
  priceInput.setAttribute('type', 'number')
  priceInput.setAttribute('step', '0.01')
  priceInput.setAttribute('value', order_product.price)

  orderIdCell.appendChild(orderIdSelect);
  productIdCell.appendChild(productIdSelect);
  quantityCell.appendChild(quantityInput);
  priceCell.appendChild(priceInput);

  updateButton.addEventListener('click', () => {
    const dataForAdd = {
      order_id: orderIdSelect.value, 
      product_id: productIdSelect.value, 
      quantity: quantityInput.value,
      price: priceInput.value
    };

    fetch(orderItemsUrl + '/' + idCell.textContent, {
      method: 'PUT',
      body: JSON.stringify(dataForAdd),
      headers: {
        'Content-Type': 'application/json'
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
      fillTableContainer_orderItems(data);
    })
    .catch(error => {
      console.error('Произошла ошибка при отправке запроса на сервер', error);
    });
  })

  deleteButton.addEventListener('click', () => {
    fetch(orderItemsUrl + '/' + idCell.textContent, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json'
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
      fillTableContainer_orderItems(data);
    })
    .catch(error => {
      console.error('Произошла ошибка при отправке запроса на сервер', error);
    });
  })
  
  updateButtonCell.appendChild(updateButton);
  deleteButtonCell.appendChild(deleteButton);

  row.appendChild(idCell);
  row.appendChild(orderIdCell)
  row.appendChild(productIdCell)
  row.appendChild(quantityCell)
  row.appendChild(priceCell)
  row.appendChild(updateButtonCell)
  row.appendChild(deleteButtonCell)

  tableBody.appendChild(row);
}

function addButton_orderItems(tableBody, ordersArr, productsArr) {
  const row = document.createElement('tr');
  const idCell = document.createElement('td');
  const orderIdCell = document.createElement('td');
  const productIdCell = document.createElement('td');
  const quantityCell = document.createElement('td');
  const priceCell = document.createElement('td');


  const addButtonCell = document.createElement('td');
  const addButton = document.createElement('button');
  addButton.textContent = 'Add';

  const orderIdSelect = document.createElement('select')
  const firstOrderOp = document.createElement('option')
  firstOrderOp.setAttribute('selected', '');
  firstOrderOp.setAttribute('hidden', '');
  firstOrderOp.textContent = 'Choose order ID'
  orderIdSelect.appendChild(firstOrderOp);
  ordersArr.forEach(item => {
    let op = document.createElement('option')
    op.setAttribute('value', item.order_id)
    op.textContent = item.order_id
    orderIdSelect.appendChild(op)
  });

  const productIdSelect = document.createElement('select')
  const firstProductOp = document.createElement('option')
  firstProductOp.setAttribute('selected', '');
  firstProductOp.setAttribute('hidden', '');
  firstProductOp.textContent = 'Choose product'
  productIdSelect.appendChild(firstProductOp);
  productsArr.forEach(item => {
    let op = document.createElement('option')
    op.setAttribute('value', item.product_id)
    op.textContent = item.product_name
    productIdSelect.appendChild(op)
  });

  const quantityInput = document.createElement('input')
  quantityInput.setAttribute('type', 'number')
  quantityInput.setAttribute('step', '1')
  quantityInput.setAttribute('value', 0)

  const priceInput = document.createElement('input')
  priceInput.setAttribute('type', 'number')
  priceInput.setAttribute('step', '0.01')
  priceInput.setAttribute('value', 0.00)

  orderIdCell.appendChild(orderIdSelect);
  productIdCell.appendChild(productIdSelect);
  quantityCell.appendChild(quantityInput);
  priceCell.appendChild(priceInput);


  addButton.addEventListener('click', () => {
    const dataForAdd = {
      order_id: orderIdSelect.value, 
      product_id: productIdSelect.value, 
      quantity: quantityInput.value,
      price: priceInput.value
    };

    fetch(orderItemsUrl, {
      method: 'PUT',
      body: JSON.stringify(dataForAdd),
      headers: {
        'Content-Type': 'application/json'
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
      fillTableContainer_orderItems(data);
    })
    .catch(error => {
      console.error('Произошла ошибка при отправке запроса на сервер', error);
    });
  });

  addButtonCell.appendChild(addButton);

  row.appendChild(idCell);
  row.appendChild(orderIdCell);
  row.appendChild(productIdCell);
  row.appendChild(quantityCell);
  row.appendChild(priceCell);
  row.appendChild(addButtonCell);
  tableBody.appendChild(row);
}

function fillTableContainer_orderItems(data) {
  clearHtml()
  tableContainer.innerHTML = `
    <table>
      <thead>
        <tr>
          <th></th>
          <th>Order</th>
          <th>Item</th>
          <th>Quantity</th>
          <th>Price</th>
        </tr>
      </thead>
      <tbody>
      </tbody>
    </table>
      `
  let arr = data["order_items"];
  let ordersArr = data["orders"];
  let productsArr = data["products"];
  const tableBody = tableContainer.querySelector('tbody');

  arr.forEach(item => addRow_orderItems(item, tableBody, ordersArr, productsArr));
  addButton_orderItems(tableBody, ordersArr, productsArr);
}

orderItemsButton.addEventListener('click', () => {
  fetch(orderItemsUrl)
    .then(response => response.json())
    .then(data => {
      console.log(data);
      fillTableContainer_orderItems(data);
})});