<template>
    <div class="signin-wrapper" :class="{'scroll-fixed':fixedScroll}">
        <div class="signin-container">
            <div class="flex-wrapper">
                <p class='title-white'>ユーザー登録</p>
                <Progress
                v-if='showProgress'
                />
            </div>
            <div v-if="showSellect" class="country-select">
                <div class='country-relative'>
                    <div class="close-container">
                        <div @click="showSelectionFalse()" class="close">
                            <i class="fas fa-times"></i>
                        </div>
                    </div>
                    <p class='country-title'>出身国を選んでください</p>
                    <p v-if="viewableCountry" class="addedCountry">{{ viewableCountry }}</p>
                    <div
                    class='each-country'
                    @click="addCountry(countryData[num-1][num-1].J_name)"
                    v-for="(num,countryindex) of countryData.length"
                    v-bind:key="countryindex">
                        <p v-if="userData.country!=countryData[num-1][num-1].J_name" >{{countryData[num-1][num-1].J_name}}</p>
                    </div>
                </div>
            </div>
            <div :class="{'slide-in':slideIn,'slide-out':slideOut}" id="slide">
                <form v-if='showProgress' @submit.prevent='submitForm' class="field-wrapper">
                    <div class="field">
                        <div class="input-box" ref='formName'>
                            <i class="fas fa-robot" id='in-font'><input required class="text-box" type='text' v-model='userData.username' id='Username' placeholder="Username"></i>
                        </div>       
                    </div>
                    <div class="field">
                        <div class="input-box" ref='formMail'>
                            <i class="far fa-envelope" id='in-font'><input required class="text-box" type='email' v-model='userData.email' id='E-mail' placeholder="E-mail"></i>
                        </div>         
                    </div>
                    <div class="field">
                        <div class="input-box">
                            <i class="far fa-envelope" id='in-font'><input required class="text-box" type='email' v-model='userData.email2' id='Confirm' placeholder="Confirm"></i>
                        </div>         
                    </div>
                    <!-- <div class="field">
                        <div @click="showSelectionTrue()" class="input-box">
                            <input required class="text-box select-dammy-box" type='text' :focus='false' v-model='viewableCountry' placeholder="Country">
                            <i class="fas fa-globe" id='in-font'>                            
                            </i>
                            <p v-if='viewableCountry' id='infont-text'>{{ viewableCountry }}</p>
                            <p v-if='!userData.country' class='down'>⌵</p>
                        </div>         
                    </div> -->
                    <div v-if='mailError||nameError||mailInUseError' class='error-form'>
                        <i class="fas fa-exclamation-triangle"></i>
                        <div v-if='mailError'>{{ mailError}}</div>
                        <div v-if='nameError'>{{ nameError }}</div>
                        <div v-if='mailInUseError'>{{ mailInUseError }}</div>
                    </div>
                    <div>
                        <button class='fbottun' ref='bform' id=''>次へ</button>
                    </div>
                    <div class="signup-footer">
                        <p>アカウントをお持ちですか</p>
                        <router-link :to="{ name: 'Login'}" class="to-login">ログイン画面へ移動=></router-link>
                        <a class="logo-container">
                            <GoogleButton
                            class='google-button'/>
                        </a>
                    </div>
                </form>
            </div>
            <transition name="slide-in">
                <Password
                class="components"
                v-if='$store.state.step==2&&showPassword&&!showEdit'
                @handle='showProgressHandler'
                @confHandle='showRegiConfHandler'
                />
            </transition>
            <transition name="notice">
                <RegisterConfirm
                class="registaer-confirm"
                v-if='$store.state.step==2&&showRegiConf&&!showEdit&&!showSent'
                :viewableCountry="viewableCountry"
                @handle='showProgressHandler'
                @edithandle='showEditHandler'
                @sentHandle='showSentHandler'
                @showPasswordFalse='showPasswordFalse'
                />
            </transition>
            <transition name="notice">
            <Sent
                v-if='showSent&&$store.state.step==3'
                @handle='showProgressHandler'
                @sentHandle='showSentHandler'
                />
            </transition>
            <transition name="slide-in">
                <Edit
                    v-if='showEdit&&!showPassword'
                    @handle='showProgressHandler'
                    @confHandle='showRegiConfHandler'
                    @edithandle='showEditHandler'
                    @setCountryForEdit="setCountryForEdit"
                    :showProgress='showProgress'
                    :viewableCountry='viewableCountry'
                    :countryData='countryData'/>
            </transition>
        </div>
    </div>
</template>

<script>
import {mapGetters,mapActions} from 'vuex'
import Progress from '@/components/signin/Progress.vue'
import Sent from '@/components/signin/Sent.vue'
import ID from '@/components/signin/ID.vue'
import Password from '@/components/signin/Password.vue'
import RegisterConfirm from '@/components/signin/RegisterConfirm.vue'
import Registered from '@/components/signin/Registered.vue'
import Edit from '@/components/signin/Edit.vue'
import GoogleButton from '@/components/signin/GoogleButton.vue'


export default {
    beforeRouteLeave (to, from, next) {
        const whileGoogleLogin = this.$store.getters.getGoogleLogin;
        if(this.filled&&!whileGoogleLogin&&!this.getUserCannotCreateError){
            let answer = window.confirm("本当に離れますか？　保存されていないデータは破棄されます。")
            if (answer) {
                next()
            } else {
                next(false)
            }
        }else{
            next(true)
        }
    },
    components:{
        Progress,
        Sent,
        ID,
        Password,
        RegisterConfirm,
        Registered,
        Edit,
        GoogleButton
    },
    data(){
        return{
            step:0,
            userData:{
                username:'',
                email:'',
                email2:'',
                country:'',
            },
            viewableCountry:'',
            nameError:null,
            mailError:null,
            mailInUseError:null,
            showSent: false,
            showProgress:true,
            showButton:true,
            showRegiConf:false,
            showEdit:false,
            showPassword: false,
            slideIn:true,
            slideOut:false,
            showSellect:false,     
            filled: false,
            googleClicked: false,
        }
    },
    updated(){
        this.showButtonHandler()
        this.filled=true
        console.log(this.$store.state.signup.username)
        // this.getClass()
    },
    created(){
        // let a = window.addEventListener("beforeunload",this.confirmFun());
        // console.log('created',a)
    },
    beforeMount() {
        this.$store.commit('setIsLoading', false)
    },
    mounted(){
        this.scrollTop()
        window.addEventListener('beforeunload',this.handleBeforeUnload)
        this.$store.commit('handleOnSigningup')
        // console.log('mounted',this.country)
        this.step = this.$store.state.step
    },
    beforeUnmount(){
        window.removeEventListener('beforeunload',this.handleBeforeUnload)
        this.$store.commit('stepClear')
        this.$store.commit('handleOnSigningup')
        this.$store.commit('fixedScrollFalse')
    },
    watch:{
        showButton:function(v) {if (v == false) { this.$refs.bform.classList.add('button-hover')}
        else{this.$refs.bform.classList.remove('button-hover')}},
        nameError:function(v) {if (v != '') { this.$refs.formName.classList.add('form-error')}
        else{this.$refs.formName.classList.remove('form-error')}},
        mailError:function(v) {if (v != '') { this.$refs.formMail.classList.add('form-error')}
        else{this.$refs.formName.classList.remove('form-error')}},
        mailInUseError:function(v) {if (v != '') { this.$refs.formMail.classList.add('form-error')}
        else{this.$refs.formName.classList.remove('form-error')}},
    },
    computed: mapGetters(['fixedScroll', 'getUserCannotCreateError']),
    methods:{
        test () {
      console.log('test')
    },
        async submitForm(){
            // validate email
            // console.log('clicked1')
            this.mailInUseError = ''
            this.nameError = this.userData.username.length < 21 ?
            '' : '@name must be less than 20 chars'
            this.mailError = this.userData.email == this.userData.email2 ?
            '' : '@addresses are not the same'
            console.log(this.nameError)
            if (this.nameError == ''&& this.mailError ==''){
                await this.$store.dispatch('checkEmail',this.userData.email)
                this.mailInUseError = this.$store.state.signup.checkedEmail ?
                '' : '@address is already in use'
                if (this.$store.state.signup.checkedEmail == true){
                    // this.showSentHandler()
                    this.handleSlide()
                    this.showPasswordTrue()
                    this.showProgressHandler()
                    this.$store.commit('addStep')
                    this.$store.commit('getUsername',this.userData.username)
                    this.$store.commit('getEmail',this.userData.email)
                    this.$store.commit('getEmail2',this.userData.email2)
                    this.$store.commit('getCountry',this.userData.country)
                }                
            }
        },
        showSentHandler(){
            this.showSent = !this.showSent
        },
        showProgressHandler(){
            this.showProgress = !this.showProgress
        },
        showRegiConfHandler(){
            this.showRegiConf = !this.showRegiConf
        },
        showEditHandler(){
            this.showEdit = !this.showEdit
        },
        progressOff(){
            this.showProgress = false
        },
        showButtonHandler(){
            if(this.userData.username!=''&&
                this.userData.mail!=''&&
                this.userData.email2!=''){
                    this.showButton = false
            }
            else{
                this.showButton = true
            }
        },
        getFilledItems(item){
            if(item == 'Username'){
                if(this.$store.signup.state.username !=''){
                    this.userData.username = this.$store.signup.state.username
                }
            }
            if(item == 'E-mail'){
                if(this.$store.signup.state.email !=''){
                    this.userData.email = this.$store.signup.state.email
                }
            }
            if(item == 'Confirm'){
                if(this.$store.signup.state.email2 !=''){
                    this.userData.email2 = this.$store.signup.state.email2
                }
            }
            // if(item == 'Country'){
            //     if(this.$store.signup.state.country !=''){
            //         this.userData.country = this.$store.signup.state.country
            //     }
            // }
        },
        showPasswordTrue(){
            this.showPassword = true
        },
        showPasswordFalse(){
            this.showPassword = false
        },
        handleSlide(){
            this.slideOut = !this.slideOut
            this.slideIn = !this.slideIn
            // var slide = document.getElementById('slide')
            // slide.setAttribute('style','display:none')
            // console.log('slide',slide)
        },
        googleLogin(){
            this.$store.dispatch('googleLogin')
        },
        showSelectionTrue(){
            this.showSellect = true
            // this.$store.commit('showModalTrue')
            // this.$store.commit('fixedScrollTrue')
        },
        showSelectionFalse(){
            this.showSellect = false
            // this.$store.commit('showModalFalse')
            // this.$store.commit('fixedScrollFalse')
        },
        addCountry(country){
            this.country = this.convertCountryToTwoCode(country)
            this.viewableCountry = country
            console.log('check',this.viewableCountry,this.country)
            this.showSelectionFalse()
        },
        convertCountryToTwoCode(country){
            console.log('in', this.countryData.length)
            for(let i = 0; i<this.countryData.length; i++){
                console.log('convert',this.countryData[i][i].J_name,country)
                if(this.countryData[i][i].J_name == country){
                    return this.countryData[i][i].two_code
                }
            }
        },
        setCountryForEdit(country){
            this.viewableCountry = country
        },
        // beforeRouteLeave (to, from, next) {
        //     if (window.confirm("Do you really want to leave?")) {
        //         window.open("exit.html", "Thanks for Visiting!");
        //         console.log('yes')
        //     }else{
        //         console.log('no')
        //     }
        //     },
        handleBeforeUnload(e){
            e.preventDefault()
            const message =
                "Are you sure you want to leave? All provided data will be lost.";
            e.returnValue = message;
            return e.returnValue;
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
    .signin-wrapper{
        width:100%;
        // height: 100vh;
        // padding-top:5rem;
        .signin-container{
            width:100%;
            height: 100vh;
            position: relative;
            flex-direction: column;
            display: flex;
            align-items: center;
            .country-select{
                position: absolute;
                width: 85%;
                max-width: 400px;
                height: 75%;
                max-height: 500px;
                border: solid grey;
                border-top: 0.3rem solid grey;
                border-bottom: 0.3rem solid grey;
                top: 2rem;
                margin-top: 0.1rem;
                margin-bottom: 0.5rem;
                padding-top: 1rem;
                padding-bottom: 1rem;
                min-height: 5rem;
                background: $back-tr-white;
                transition: .5s;
                z-index: 1;
                overflow: scroll;
                .country-relative{
                    position: relative;
                    .close-container{
                        margin-top: -1rem;
                        .close{
                            // position: sticky;
                        }
                    }
                    .country-title{
                        margin-top: 1.5rem;
                        padding-bottom: 1rem;
                    }
                    .addedCountry{
                            // background: red;
                            margin-bottom: 0.5rem;
                            font-weight: bold;
                            background: rgba(162, 161, 161, 0.3);
                        }
                    .each-country{
                        font-size: 0.8rem;
                        margin-top: 0.1rem;
                        margin-bottom: 0.1rem;
                        transition: .5s;
                    }
                    .each-country:hover{
                        background: $lite-gray;
                        
                    }
                }
            }
            .title-white{
                margin-bottom: 1rem;
            }
        }
    }
    .signin-text{
        color:white;
        font-size:2rem;
       
    }
    .field-wrapper{
        // display: flex;
        // flex-direction: column;
        // justify-content: center;
        margin-top:3rem;
    }
    .field{
        display: flex;
        justify-content: center;
        align-items: center;
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
    input[type="text"]:focus {
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
        position: relative;
        .down{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            -webkit-transform: translate(-50%, -50%);
            -ms-transform: translate(-50%, -50%);
            color:rgb(75, 75, 75);
            
        }
    }
    #in-font{
        margin-left:0.5rem;
        color:rgb(158, 158, 158); 
        transition:0.3s;
        position:relative;
    }
    #infont-text {
        font-size: 0.8rem;
        margin-left:0.5rem;
        color:rgb(75, 75, 75);
        font-weight: 450;
        transition:0.3s;
        font-style: italic;
    }
    ::placeholder {
        font-style: italic;
        color:rgb(75, 75, 75);
        margin-left:0.5rem;
        font-weight: 400;
        transition:0.3s;
    }
    #in-font:focus-within{
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
.components{
    display: absolute;
}
#slide{
    display: absolute;
}
// .slide-in{
// 	text-align: center;
// 	opacity: 0;
// 	animation: slide-in-anim 1.5s ease-out forwards;
// }
.slide-out{
    text-align: center;
	opacity: 1;
	animation: slide-out-anim 1.5s ease-out forwards;
}
.signup-footer{
    p{
        color: white;
        margin-top: 0.5rem;
        font-weight: bold;
    }
    .to-login:hover{
        background: rgba(252, 252, 252, 0.3);
        font-weight: bold;
    }
    .to-login{
        display: inline-block;
        color: $lite-gray;
        padding: 0.2rem 0.5rem;
        margin: 0.4rem;
        border: solid $base-color;
        transition: .5s;
    }
    .logo-container{
        display: flex;
        justify-content: center;
        .google-button{
            width: 70%;        
        }
    }
}
.select-dammy-box{
    caret-color: transparent;
    margin-left: 1rem;
}
// @keyframes slide-in-anim {
// 	0% {
// 		opacity: 0;
//         transform: translateX(-20%);
// 	}
// 	// 60% {
// 	// 	transform: translateX(-10%);
// 	// }
// 	// 75% {
// 	// 	transform: translateX(2%);
// 	// }
// 	100% {
// 		opacity: 1;
// 		transform: translateX(0);
// 	}
// }
@keyframes slide-out-anim {
	0% {
		opacity: 1;
        transform: translateX(0);
	}
	// 60% {
	// 	transform: translateX(-10%);
	// }
	// 75% {
	// 	transform: translateX(2%);
	// }
	100% {
		opacity: 0;
		transform: translateX(-60%);
        display: none;
        
	}
}
.registaer-confirm{
    z-index: 1;
}
.slide-in-enter-active {
  animation: slide-in  ease-out 1.5s;
}
.slide-in-leave-active {
  animation: slide-out ease-out 1.5s;
}
@keyframes slide-in {
  0% {
		opacity: 0;
        transform: translateX(5%);
	}
	// 60% {
	// 	transform: translateX(-10%);
	// }
	// 75% {
	// 	transform: translateX(2%);
	// }
	100% {
		opacity: 1;
		transform: translateX(0);
	}
}
@keyframes slide-out {
  0% {
		opacity: 1;
        transform: translateX(0);
	}
	// 60% {
	// 	transform: translateX(-10%);
	// }
	// 75% {
	// 	transform: translateX(2%);
	// }
	100% {
		opacity: 0;
		transform: translateX(-10%);
	}
}
</style>