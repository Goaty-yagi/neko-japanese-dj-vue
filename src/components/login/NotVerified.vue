<template>
    <div class="account-wrapper l-wrapper">
        <div class="main-wrapper">
            <div class='main-notification-wrapper'>
                <div class='main-notice-wrapper'>
                    <div class="close-container">
                        <div v-if="!currentPageName" @click="unShow()" class="close">
                            <i class="fas fa-times"></i>
                        </div>
                    </div>
                    <img @click="backHome()" class='main-image' src="@/assets/logo.png">
                    <div v-if="sent">
                        <div v-if='asyncActionEndObj.success' class="success">
                            <p class='main-text1'>パスワード再登録メールを送信しました。</p>
                            <p class='main-text1'>登録したアドレスで確認してください。</p>
                        </div>
                        <div v-if='!asyncActionEndObj.success' class="success">
                            <p class='main-text1'>パスワード再登録メールの送信に失敗しました。</p>
                            <p class='main-text1'>しばらく経ってからもう一度お試しください。</p>
                        </div>
                    </div>
                    <div v-if="!sent&&!sending">
                        <p class='main-text1'>メール承認が完了していません。</p>
                        <p class='main-text1'>メール承認を完了してください。</p>
                    </div>
                    <div v-if="sending" class="spinner">
                        <i class="fas fa-spinner fa-pulse"></i>
                    </div>
                    <button v-if="!sent&&!sending" @click='resent' onclick="disabled = true" class='btn-gray-black-gray-sq'>承認メールを送る</button>                      
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import {router} from "@/main.js"
export default {
    props:[
        'currentPageName',
    ],
    data(){
        return{
            sent: false,
            sending: false
        }
    },
    mounted() {
        console.log("MOUN",this.asyncActionEndObj.success)
        this.sent = false
        this.top = window.scrollY
        document.body.style.top = `-${window.scrollY}px`;
        document.body.style.position = 'fixed'
    },
    beforeUnmount() {
        document.body.style.position = ''
        window.scrollTo(0, this.top)
        this.$store.commit('resetetAsyncActionEndObj')
    },
    computed:{
        user() {
            return this.$store.state.signup.user;
        },
        asyncActionEndObj() {
            return this.$store.getters.getAsyncActionEndObj
        }

    },
    methods:{
        async resent(){
            this.sending = true
            await this.$store.dispatch('sendEmailVerify', this.user.UID)
            this.sent = true
            this.sending = false
        },
        backHome(){
            router.push('/' )
        },
        unShow(){
            this.$emit('handleShowEmailVerified')
        }
    }
}
</script>

<style lang="scss" scoped>
@import "style/_variables.scss";

.account-wrapper{
    width: 100%;
    .main-wrapper{
        display: flex;
        justify-content: center;
    }
}
.btn-gray-black-gray-sq{
    margin-bottom: 2rem;
    font-size: 1.2rem;
    padding-right: 0.5rem;
    padding-left: 0.5rem;
}
img{
    margin-top: 1.5rem;
    cursor: pointer;
}
.main-notification-wrapper{
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
}
    .main-notice-wrapper{
        position: relative;
        border: solid $base-color;
        border-radius: 2vh;
        background:$back-white;
        text-align: center;       
        position:relative;
        width: 90%;
        min-height: 430px;
    }
    .main-image{
        width:15%;
        height:auto;
        margin-left: auto;
        margin-right: auto;
    }
    .main-text1{
        font-size:1.4rem;
        font-weight: bold;
        margin:2rem;
    }
.spinner {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%,-50%);
    width: 100%;
    font-size: 3rem;
}
</style>