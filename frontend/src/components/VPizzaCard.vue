<template>
  <div class="pizza-card">
    <div class="pizza-card__info">
        <svg width="30" height="30" viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg" @click="$emit('openModal')">
        <path fill-rule="evenodd" clip-rule="evenodd" d="M15 3C8.37258 3 3 8.37258 3 15C3 21.6274 8.37258 27 15 27C21.6274 27 27 21.6274 27 15C27 8.37258 21.6274 3 15 3ZM15 23.2505C14.1716 23.2505 13.5 22.579 13.5 21.7505V12.7985C13.5 11.97 14.1716 11.2985 15 11.2985C15.8284 11.2985 16.5 11.97 16.5 12.7985V21.7505C16.5 22.579 15.8284 23.2505 15 23.2505ZM13.5 8.24859C13.5 7.4207 14.1716 6.74957 15 6.74957C15.8284 6.74957 16.5 7.4207 16.5 8.24859C16.5 9.07647 15.8284 9.74761 15 9.74761C14.1716 9.74761 13.5 9.07647 13.5 8.24859Z" fill="#BF0200"/>
        <path fill-rule="evenodd" clip-rule="evenodd" d="M3 15C3 8.37258 8.37258 3 15 3C21.6274 3 27 8.37258 27 15C27 21.6274 21.6274 27 15 27C8.37258 27 3 21.6274 3 15ZM15 0C6.71573 0 0 6.71573 0 15C0 23.2843 6.71573 30 15 30C23.2843 30 30 23.2843 30 15C30 6.71573 23.2843 0 15 0Z" fill="#BF0200"/>
        </svg>
    </div>
    <img src="../img/pizza.png" class="pizza_pic"/>
    <span class="card-title">{{ name }}</span>
    <span class="card-price">{{ price }}руб.</span>
    <VButtonRed :title="'добавить'" :click="'add'" @add="addToBasket"></VButtonRed>
    <VAddModal
        :isVisible="isModalVisible"
        :title="modalTitle"
        @close="closeModal"
    ></VAddModal>
  </div>
</template>

<script>
import axios from 'axios';
import VButtonRed from './VButtonRed.vue';
import VAddModal from './VAddModal.vue';

export default {
    name: 'VPizzaCard',
    components: {
        VButtonRed,
        VAddModal,
    },
    data() {
        return {
            pizzas: [], // Массив для хранения пицц
            error: null, // Переменная для хранения ошибок
            isModalVisible: false,
            modalTitle: null,
        };
    },
    methods: {
        async addToBasket(){
            try {
                const response = await axios.post(`http://localhost:8001/users/add_to_cart?email=user%40example.com&pizza_id=${this.id}&count=1`, {
                    email: 'user@example.com',
                    pizza_id: this.id,
                    count: 1,
                }); 
                console.log(response.data);
                this.openAddModal();
            } catch (error) {
                this.error = 'Ошибка при получении пицц: ' + error.message; // Обработка ошибок
                console.error('Ошибка при получении пицц:', error);
            }
        },
        openAddModal() {
            this.modalTitle = 'Товар добавлен в корзину!';
            this.isModalVisible = true;
        },
        closeModal() {
            this.isModalVisible = false;
        },

    },
    props: {
        name: String,
        price: Number,
        id: String,
    } 
  }
  // props: {
  //   msg: String
  // } тут надо по клику модалку вызывать ещё
</script>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.pizza-card{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 390px;
  width: 250px;
  background-color: #FFEFD2;
  border: 3px solid #BF0200;
  border-radius: 30px;
  padding: 20px;
  margin: 20px 0;
  
}
.pizza_pic{
  height: 235px;
  width: 224px;
}
.card-title{
  font-family: Nunito;
  font-size: 2.2rem;
  color: #CA151C;
}
.card-price{
  font-family: Nunito;
  font-size: 1.7rem;
  color: #CA151C;
  font-weight: 300;
}
.pizza-card__info{
  align-self: flex-end;
  /* margin: 0px 15px; */
  margin-bottom: -30px;
  z-index: 1;
}
.button-red{
    width: 100%;
}
</style>
