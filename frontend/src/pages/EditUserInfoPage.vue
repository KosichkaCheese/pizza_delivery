<template>
    <div class="LK-page">
        <VHeader :title="'личный кабинет *'" :toLink="'/'"></VHeader>
        <div class="LK-page__content">
            <div class="user-info">
                <div class="user-info__input">
                    <input class="order-input__name" v-model="userName" required>
                </div>
                <div class="user-info__input">
                    <span><b>Адрес:</b></span><input class="order-input" v-model="userAddress" required>
                </div>
                <div class="user-info__input">
                    <span class="order-input__label"><b>Номер телефона:</b></span><input class="order-input" v-model="userPhone" required>
                </div>
                <span><b>Почта:</b> {{ user.email }}</span>
            </div>
            <div class="UserEdit-page__actions">
                <RouterLink to="/LK" class="UserEdit-page__link">
                    <VButtonWhite :title="'отмена'" class="UserEdit-button"></VButtonWhite>
                </RouterLink>
                <VButtonRed :title="'сохранить'" class="UserEdit-edit-button" :click="'save'" @save="saveUserInfo"></VButtonRed>
            </div>
        </div>
        <VExitModal
            :isVisible="isModalVisible"
            :title="modalTitle"
            @close="closeModal"
        ></VExitModal>
    </div>
</template>

<script>
import VHeader from '../components/VHeader.vue';
import VButtonWhite from '../components/VButtonWhite.vue';
import VButtonRed from '../components/VButtonRed.vue';
import VExitModal from '../components/VExitModal.vue';

import axios from 'axios';

export default {
    name: 'EditUserInfoPage',
    components: {
        VButtonRed,
        VHeader,
        VButtonWhite,
        VExitModal,
    },
    data(){
        return {
            user: [],
            error: null,
            orders: [],
            ordersPizzas: [],
            isModalVisible: false,
            modalTitle: null,
            userName:null,
            userAddress: null,
            userPhone: null,
        };
    },
    methods: {
        async getUser() {
            try {
                const response = await axios.get('http://localhost:8001/users/get_user?email=user%40example.com'); // Замените на ваш URL
                this.user = response.data.data;
                this.userName = this.user.name;
                this.userAddress = this.user.address;
                this.userPhone = this.user.phone;
            } catch (error) {
                this.error = 'Ошибка при получении пицц: ' + error.message; // Обработка ошибок
                console.error('Ошибка при получении пицц:', error);
            }
        },
        exitModal(){
            this.modalTitle = 'Вы действительно хотите выйти?';
            this.isModalVisible = true;
        },
        closeModal() {
            this.isModalVisible = false;
        },
        async saveUserInfo(){
            try {
                const response = await axios.put(`http://localhost:8001/users/update_user`, {
                    email: this.user.email,
                    name: this.userName,
                    address: this.userAddress,
                    phone: this.userPhone,
                });
                console.log(response.data.data);
                this.$router.push('/LK');
            } catch (error) {
                this.error = 'Ошибка при получении пицц: ' + error.message; // Обработка ошибок
                console.error('Ошибка при получении пицц:', error);
            }
        }
    },
    created(){
        this.getUser();
    }
}
</script>

<style>
.LK-page{
    color: #CA151C;
    font-family: Nunito;
    overflow-x: hidden;
    width:100%;
    height:100%;
}
.LK-page__content{
    margin: 0 90px;
}
.user-info{
    display:flex;
    flex-direction: column;
    margin: 10px 0;
    font-size: 1.7rem;
    justify-content:space-around;
    height: 30%;
    font-weight: 300;
}
.user-info__name{
    font-weight: 800;
    font-size: 2.3rem;
}
.user-orders__title{
    margin: 10px 0;
    font-weight: 800;
    font-size: 2.5rem;
}
.UserEdit-page__actions{
    display: flex;
    justify-content: space-between;
    /* margin: 100px 0 30px 0; */
    margin: 240px 0 30px 0;
    width: 100%;
}
.UserEdit-edit-button, .UserEdit-page__link{
    width: 40%;
}
.UserEdit-button{
    width: 100%;
}
.user-info__input{
    width: 60%;
}
.order-input__label{
    width: 50%;
}
.order-input{
    width: 100%;
}
.order-input__name{
    background: none;
    border: solid 3px #BF0200;
    min-height: 30px;
    width: 50%;
    border-radius: 20px;
    font-family: Nunito;
    color: #CA151C;
    padding: 3px 20px;
    margin: 10px 0;
    font-weight: 800;
    font-size: 2.3rem;
    width: 100%;
}
.order-input:focus{
    outline: none;
}
</style>
