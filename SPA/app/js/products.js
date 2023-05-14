const productsButton = document.querySelector('#products');
tableContainer = document.querySelector('#table-container');
const productsUrl = '/api/products'

function clearHtml() {
  tableContainer.innerHTML = '';
}

function addRow_products(item, tableBody) {
  const row = document.createElement('tr');
  const idCell = document.createElement('td');
  idCell.textContent = item.product_id;
  const productNameCell = document.createElement('td');
  const brandCell = document.createElement('td');
  const categoryCell = document.createElement('td');
  const descriptionCell = document.createElement('td');
  const priceCell = document.createElement('td');
  const stockQuantityCell = document.createElement('td');

  const updateButtonCell = document.createElement('td');
  const updateButton = document.createElement('button');
  updateButton.textContent = 'Update';

  const deleteButtonCell = document.createElement('td');
  const deleteButton = document.createElement('button');
  deleteButton.textContent = 'Delete';

  const productNameInput = document.createElement('input')
  productNameInput.setAttribute('type', 'text')
  productNameInput.setAttribute('value', item.product_name);
  const brandInput = document.createElement('input')
  brandInput.setAttribute('type', 'text')
  brandInput.setAttribute('value', item.brand);
  const categoryInput = document.createElement('input')
  categoryInput.setAttribute('type', 'text')
  categoryInput.setAttribute('value', item.category);
  const descriptionInput = document.createElement('input')
  descriptionInput.setAttribute('type', 'text')
  descriptionInput.setAttribute('value', item.description);
  const priceInput = document.createElement('input')
  priceInput.setAttribute('type', 'number')
  priceInput.setAttribute('step', 0.01)
  priceInput.setAttribute('value', item.price);
  const stockQuantityInput = document.createElement('input')
  stockQuantityInput.setAttribute('type', 'number')
  stockQuantityInput.setAttribute('step', 1)
  stockQuantityInput.setAttribute('value', item.stock_quantity);

  productNameCell.appendChild(productNameInput);
  brandCell.appendChild(brandInput);
  categoryCell.appendChild(categoryInput);
  descriptionCell.appendChild(descriptionInput);
  priceCell.appendChild(priceInput);
  stockQuantityCell.appendChild(stockQuantityInput);

  updateButton.addEventListener('click', () => {
    const dataForAdd = {
      product_name: productNameInput.value, 
      brand: brandInput.value, 
      category: categoryInput.value, 
      description: descriptionInput.value,
      price: priceInput.value,
      stock_quantity: stockQuantityInput.value
    };
    const jwt_token = localStorage.getItem('jwt_token');

    fetch(productsUrl + '/' + idCell.textContent, {
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
      fillTableContainer_products(data);
    })
    .catch(error => {
      console.error('Произошла ошибка при отправке запроса на сервер', error);
    });
  })

  deleteButton.addEventListener('click', () => {
    const jwt_token = localStorage.getItem('jwt_token');

    fetch(productsUrl + '/' + idCell.textContent, {
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
      console.log(data);
      fillTableContainer_products(data);
    })
    .catch(error => {
      console.error('Произошла ошибка при отправке запроса на сервер', error);
    });
  })

  updateButtonCell.appendChild(updateButton);
  deleteButtonCell.appendChild(deleteButton);

  row.appendChild(idCell);
  row.appendChild(productNameCell);
  row.appendChild(brandCell);
  row.appendChild(categoryCell);
  row.appendChild(descriptionCell);
  row.appendChild(priceCell);
  row.appendChild(stockQuantityCell)
  row.appendChild(updateButtonCell);
  row.appendChild(deleteButton);
  tableBody.appendChild(row);
}

function addButton_products(tableBody) {
  const row = document.createElement('tr');
  const idCell = document.createElement('td');
  const productNameCell = document.createElement('td');
  const brandCell = document.createElement('td');
  const categoryCell = document.createElement('td');
  const descriptionCell = document.createElement('td');
  const priceCell = document.createElement('td');
  const stockQuantityCell = document.createElement('td');

  const addButtonCell = document.createElement('td');
  const addButton = document.createElement('button');
  addButton.textContent = 'Add';

  const productNameInput = document.createElement('input')
  productNameInput.setAttribute('type', 'text')
  const brandInput = document.createElement('input')
  brandInput.setAttribute('type', 'text')
  const categoryInput = document.createElement('input')
  categoryInput.setAttribute('type', 'text')
  const descriptionInput = document.createElement('input')
  descriptionInput.setAttribute('type', 'text')
  const priceInput = document.createElement('input')
  priceInput.setAttribute('type', 'number')
  priceInput.setAttribute('step', 0.01)
  priceInput.setAttribute('value', 0.00);
  const stockQuantityInput = document.createElement('input')
  stockQuantityInput.setAttribute('type', 'number')
  stockQuantityInput.setAttribute('step', 1)
  stockQuantityInput.setAttribute('value', 0);

  productNameCell.appendChild(productNameInput);
  brandCell.appendChild(brandInput);
  categoryCell.appendChild(categoryInput);
  descriptionCell.appendChild(descriptionInput);
  priceCell.appendChild(priceInput);
  stockQuantityCell.appendChild(stockQuantityInput);

  addButton.addEventListener('click', () => {
    const jwt_token = localStorage.getItem('jwt_token');

    const dataForAdd = {
      product_name: productNameInput.value, 
      brand: brandInput.value, 
      category: categoryInput.value, 
      description: descriptionInput.value,
      price: priceInput.value,
      stock_quantity: stockQuantityInput.value
    };

    fetch(productsUrl, {
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
      fillTableContainer_products(data);
    })
    .catch(error => {
      console.error('Произошла ошибка при отправке запроса на сервер', error);
    });
  });

  addButtonCell.appendChild(addButton);

  row.appendChild(idCell);
  row.appendChild(productNameCell);
  row.appendChild(brandCell);
  row.appendChild(categoryCell);
  row.appendChild(descriptionCell);
  row.appendChild(priceCell);
  row.appendChild(stockQuantityCell)
  row.appendChild(addButtonCell);
  tableBody.appendChild(row);
}

function fillTableContainer_products(data) {
  clearHtml()
  tableContainer.innerHTML = `
    <table>
      <thead>
        <tr>
          <th></th>
          <th>Product name</th>
          <th>Brand</th>
          <th>Category</th>
          <th>Description</th>
          <th>Price</th>
          <th>Stock quantity</th>
        </tr>
      </thead>
      <tbody>
      </tbody>
    </table>
      `
  let arr = data["products"];
  const tableBody = tableContainer.querySelector('tbody');

  arr.forEach(item => addRow_products(item, tableBody));
  addButton_products(tableBody)
}

productsButton.addEventListener('click', () => {
  fetch(productsUrl)
    .then(response => response.json())
    .then(data => {
      console.log(data);
      fillTableContainer_products(data);
})});