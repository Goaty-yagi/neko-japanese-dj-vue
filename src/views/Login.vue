<template>
        <div class="login-wrapper" :class="{'scroll-fixed':fixedScroll,'laoding-center':$store.state.isLoading}">
            <div v-if="!$store.state.isLoading" class="flex-wrapper">
                <p class='title-white'>ログイン</p>
                <form class="id-form" @submit.prevent='submitForm' >
                        <div class="field">
                            <div class="input-box">
                                <i class="far fa-envelope" id='in-font'><input required class="text-box" type='email' v-model='email' id='E-mail' placeholder="E-mail"></i>
                            </div>         
                        </div>
                        <div class="field">
                            <div class="input-box">
                                <i class="fas fa-unlock-alt" id='in-font'><input required class="text-box" :type="inputType" v-model='password' placeholder="Password"></i>
                                <i :class="[passType ? 'fas fa-eye':'fas fa-eye-slash']" id='eye' @click='click' ></i>
                            </div>      
                        </div>
                        <div class='error-form'  v-if='userError||passError||manyError||emailError'>
                            <i class="fas fa-exclamation-triangle"></i>
                            <div>{{ userError }}</div>
                            <div class='pass-text-wrapper' v-if='userError'>
                                <p>ユーザー登録しますか。</p>
                                <p @click='goSignup' class="resetButton">ユーザー登録</p>
                            </div>
                            <div>{{ passError }}</div>
                             <div class='pass-text-wrapper' v-if='passError'>
                                <p>パスワードをお忘れですか。</p>
                                <p  @click='resetPass' class="resetButton" >パスワードの再設定</p>
                            </div>
                            <div>{{ manyError }}</div>
                            <div>{{ emailError }}</div>
                        </div>
                        <!-- <div class='text-wrapper' v-if='passError'>
                            <p>パスワードをお忘れですか。</p>
                            <p  @click='resetPass' class='text'>パスワードの再設定</p>
                        </div> -->
                        <!-- <div class='text-wrapper' v-if='userError'>
                            <p>ユーザー登録しますか。</p>
                            <p @click='goSignup' class='text'>ユーザー登録</p>
                        </div> -->
                        <div>
                            <button :disable='!userError||!passError||!manyError' class='fbottun' ref='bform'>ログイン</button>
                        </div>
                        <p>Googleアカウントでログイン</p>
                        <a class="logo-container">
                            <GoogleButton
                            class='google-button'/>
                        </a>
                </form>
            </div>
        <div>
        <AbstractModal
        v-if="showSentPassReset"
        :mainText='modalMessage'
        :showButton='modalShowButton'
        />
        <!-- <SentPassReset v-if='showSentPassReset'/> -->
        <!-- <NotVerified v-if='showNotVerified'
        @handleShowSent = 'handleShowSent'
         />
        <Sent v-show='showSent'/> -->
  </div>
    </div>
</template>

<script>
import {router} from "../main.js"
import SentPassReset from '@/components/login/SentPassReset.vue'
import NotVerified from '@/components/login/NotVerified.vue'
import Sent from '@/components/signin/Sent.vue'
import AbstractModal from '@/components/parts/AbstractModal.vue'
import GoogleButton from '@/components/signin/GoogleButton.vue'


export default {
    components:{
        SentPassReset,
        AbstractModal,
        Sent,
        NotVerified,
        GoogleButton
    },
    data(){
        return{
            email:'',
            password:'',
            passType:true,
            showButton:true,
            passError:null,
            userError:null,
            emailError:null,
            manyError:null,
            showSentPassReset:false,
            showSent:false,
            showNotVerified:false,
            store: this.$store.state.signup,
            fixedScroll: this.$store.getters.fixedScroll.rout,
            modalMessage:'パスワード再登録メールを送信しました。\n登録したアドレスで確認してください。',
            modalShowButton:false
        }
    },
    mounted(){
        this.scrollTop()
    },
    beforeUnmount() {
        this.$store.commit('fixedScrollFalse')
        this.$store.commit('showModalFalse')
    },
     beforeMount() {
        this.$store.commit('setIsLoading', false)
    },
    updated(){
        this.showButtonHandler()
    },
    watch:{
        showButton:function(v) {if (v == false) { this.$refs.bform.classList.add('button-hover')}
        else{this.$refs.bform.classList.remove('button-hover')}},
    },
    computed: {
        inputType: function () {
        return this.passType ? "password":"text";
            }
        },
    methods:{
        showButtonHandler(){
            if(this.password != '' &&this.email != ''){
                this.showButton = false
            }else{
                this.showButton = true
                }
            },
        click(){
            this.passType = !this.passType
        },
        goSignup(){
            this.$router.push({name:'Signup'})
        },
        handleShowSentPassReset(){
            this.$store.commit('fixedScrollTrue')
            this.$store.commit('showModalTrue')
            this.showSentPassReset = true
        },
        handleShowNotVerified(){
            this.showNotVerified = true
        },
        async resetPass(){
            this.$store.commit('setIsLoading', true)
            await this.$store.dispatch('SendChangePassword',this.email)
            .then(() => {
                this.$store.commit('setIsLoading', false)
                this.handleShowSentPassReset()
            })

        },
        handleShowSent(){
            this.showSent = true
        },
        async submitForm(){      
            
            await this.$store.dispatch('login',{
            email:this.email,
            password:this.password
            })
            .then(() => {
                try{
                    const error = this.$store.getters.getLoginError
                    const errMessage = Object.values(error)[0][0]
                    if(errMessage) {
                        this.userError = errMessage == 'user-not-found.'?
                        'ユーザーが存在しません。' : ''
                        this.emailError = errMessage == 'Enter a valid email address.'?
                        '正しいアドレスを入力してください。' : '' 
                        this.passError = errMessage == 'wrong-password.'?
                        'パスワードが違います。\nまたはメール承認が完了していません。' : ''
                        this.manyError = errMessage == 'auth/too-many-requests'?
                        '短時間にリクエストを複数受けたため一時的にリクエストを停止します。暫く経ってもう一度お試しください。' :'' 
                    }
                } catch(e) {
                    console.log("something went wrong")
                }

            })                        
        },
        googleLogin(){
            this.$store.dispatch('googleLogin')
        },
        scrollTop(){
            window.scrollTo({
                top: 0,
            });
        },
    }
}
</script>


<style scoped lang='scss'>
@import "style/_variables.scss";
.login-wrapper{
    width:100vw;
    flex-direction: column;
    display: flex;
    align-items: center;
    .id-form{
        margin-top: 2rem;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    }
    .login-text{
        color:white;
        font-size:1.2rem;
        font-weight: bold;
        margin-bottom: 1.5rem;
       
    }
    .field-wrapper{
        margin-top:3rem;
    }
    .field{
        display: flex;
        justify-content: center;
        align-items: center;
        align-self: center;
    }
    .label{
        color:white;
        width: 2.7rem;
        overflow-wrap: break-word;
        margin-right:1%;
        line-height:1rem
    }.label:not(:last-child) {
        margin-bottom: initial;
}
    input[type="password"]:focus {
        outline: none;
        }
    input[type="email"]:focus {
        outline: none;
    }
    select:focus {
        outline: none;
        }
    .input-box:focus-within{
        border: solid $base-color;
        
        }
    .input-box{
        border: 0.12rem solid $base-color;
        border-radius: 100vh;
        background: $back-white;
        width: 17rem;
        height: 3rem;
        display: flex;
        justify-content: flex-start;
        align-items: center;
        position:relative;
        
    }#in-font{
        margin-left:0.5rem;
        color:rgb(158, 158, 158); 
        transition:0.3s;
        position:relative;
    }
    #in-font:focus-within{
        color:rgb(92, 92, 92);

    }
    #eye{
        position:absolute;
        right:0;
        margin-right:0.5rem;
        color:rgb(158, 158, 158);
        transition:0.3s;
    }
    #eye:hover{
        color:rgb(92, 92, 92);
    }
    #eye:focus-within{
        color:rgb(92, 92, 92);
    }
    .text-box{
        width: 14rem;
        border:none;
        background: $back-white;
        margin-left:0.5rem;
        position:absolute;
        left:1rem;
    }
    .select-box{
        width: 82%;
        border:none;
        background: $back-white;
        margin-left:0.5rem;
    }
    
    .check-box-text{
        color:white;
        margin-left:1rem;
    }
    .text-wrapper{
        width: 100%;
        display:flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        
    }
    .text:hover{
        background: $base-white;
        color: $dark-blue;
        font-weight: bold;
    }
    .text{
        color:white;margin-top:1rem;
        border: 0.1rem solid white;
        border-radius: 0.5rem;
        width: 60%;
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
        transition:0.8s;
    }
    .error-form{
        width:95%;
        background: $back-tr-white;
        padding-bottom: 0.5rem;
        div{
            white-space: pre-wrap;
        }
    }
    p{
        color:white;
        margin-top:1rem;
    }
    .logo-container{
        display: flex;
        justify-content: center;
        .google-button{
            width: 70%;        
        }
    }
.pass-text-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 1rem;
   p{
    color: red;
   }
   .resetButton {
    color: gray;
    margin-top:1rem;
    border: 0.1rem solid gray;
    border-radius: 0.5rem;
    width: 60%;
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
    transition:0.8s;
   }
   .resetButton:hover{
        background: $base-white;
        color: $dark-blue;
        font-weight: bold;
    }
}
</style>