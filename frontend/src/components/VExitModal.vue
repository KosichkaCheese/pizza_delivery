<template>
  <div v-if="isVisible" class="modal-overlay" @click.self="close">
    <div class="modal">
        <h2>{{ title }}</h2>
        <div class="modal-content">
            <img src="../img/sticker.png" class="modal-content__pic"/>
        </div>
        <VButtonRed class="modal-button" :title="'конечно нет!'" :click="'close'" @close="close"></VButtonRed>
    </div>
  </div>
</template>

<script>
import VButtonRed from './VButtonRed.vue';

export default {
    name: 'VExitModal',
    components: {
        VButtonRed,
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
    },
    methods: {
        close() {
            this.$emit('close');
        },
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
.modal-content__pic{
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
