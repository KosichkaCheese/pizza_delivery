<template>
  <div v-if="isVisible" class="modal-overlay" @click.self="close">
    <div class="modal">
        <button @click="close" class="modal__close-button">
            <ExitSVG></ExitSVG>
        </button>
        <h2>{{ title }}</h2>
        <div class="modal-content">
            
            <img src="../img/pizza.png" class="modal-content__pizza_pic"/>
            <p class="modal-content__pizza_description"><b>описание: </b>{{ message }}</p>
        </div>
        <VButtonRed class="modal-button" :title="'добавить в корзину'" :click="'add'" @add="addToBasket"></VButtonRed>
    </div>
  </div>
</template>

<script>
import ExitSVG from '../img/exitSVG.vue';
import VButtonRed from './VButtonRed.vue';
import axios from 'axios';

export default {
    name: 'VPizzaInfoModal',
    components: {
        VButtonRed,
        ExitSVG,
    },
    props: {
        isVisible: {
            type: Boolean,
            required: true
        },
        title: {
            type: String,
            default: 'Пиццааа'
        },
        message: {
            type: String,
            default: 'Это содержимое модального окна.'
        },
        id: {
            type: String,
        }
    },
    methods: {
        close() {
            this.$emit('openAddModal');
            this.$emit('close');
            
        },
        async addToBasket(){
            try {
                const response = await axios.post(`http://localhost:8001/users/add_to_cart?email=user%40example.com&pizza_id=${this.id}&count=1`, {
                    email: 'user@example.com',
                    pizza_id: this.id,
                    count: 1,
                }); 
                console.log(response.data);
                
                this.close();
            } catch (error) {
                this.error = 'Ошибка при получении пицц: ' + error.message; // Обработка ошибок
                console.error('Ошибка при получении пицц:', error);
            }
        }
    }
};
</script>

<style>
h2{
    margin: 0;
}
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.318);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 100;
}

.modal {
    background: #FFEFD2;
    padding: 20px;
    border-radius: 40px;
    border: solid 3px #BF0200;
    text-align: center;
    font-family: Nunito;
    font-size: 1.7rem;
    color: #A60200;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.modal-button{
    width: 60%;
}
.modal__close-button{
    align-self: flex-end;
    background: none;
    border: none;
    width:fit-content;
}
.modal-content__pizza_pic{
  height: 235px;
  width: 224px;
}
.modal-content{
    display: flex;
    margin-right: 50px;
}
.modal-content__pizza_description{
    margin-left: 10px;
}
</style>
