<template>
    <div class="password-wrapper">
        <div v-if="showSellect" class="country-select">
            <div class='country-relative'>
                <div class="close-container">
                    <div @click="showSelectionFalse()" class="close">
                        <i class="fas fa-times"></i>
                    </div>
                </div>
                <p class='country-title'>出身国を選んでください</p>
                <p v-if="viewCountry" class="addedCountry">{{ viewCountry }}</p>
                <div
                class='each-country'
                @click="addCountry(countryData[num-1][num-1].J_name)"
                v-for="(num,countryindex) of countryData.length"
                v-bind:key="countryindex">
                    <p class='country-name' v-if="viewCountry!=countryData[num-1][num-1].J_name" >{{countryData[num-1][num-1].J_name}}</p>
                </div>
            </div>
        </div>
        <form class="id-form" @submit.prevent='submitForm' >
            <div class='field-wrapper'>
                <div class="field">
                    <div class="input-box">
                        <i class="fas fa-robot" id='in-font'><input required class="text-box" v-model='username' type='text' id='Username' ></i>
                    </div>       
                </div>
                <div class="field">
                    <div class="input-box">
                        <i class="far fa-envelope" id='in-font'><input required class="text-box" v-model='email' type='email'  id='E-mail' placeholder="E-mail"></i>
                    </div>         
                </div>
                <!-- <div class="field">
                        <div @click="showSelectionTrue()" class="input-box">
                            <input required class="text-box select-dammy-box" type='text' v-model='viewCountry' :placeholder="country">
                            <i class="fas fa-globe" id='in-font'>                            
                            </i>
                            <p v-if='viewCountry' id='infont-text'>{{ viewCountry }}</p>
                            <p v-if='!viewCountry' class='down'>⌵</p>
                        </div>         
                    </div>
                     -->
                <div class="field">
                    <div class="input-box">
                        <i class="fas fa-unlock-alt" id='in-font'><input required v-model='password' class="text-box" autocomplete :type="inputType"></i>
                        <i :class="[passType ? 'fas fa-eye-slash':'fas fa-eye']" id='eye' @click='click' ></i>
                    </div>      
                </div>
                <div class="field">
                    <div class="input-box">
                        <i class="fas fa-unlock-alt" id='in-font'><input required class="text-box" :type="inputType2" autocomplete v-model='password2' placeholder="Conf Password"></i>
                            <i :class="[passType2 ? 'fas fa-eye-slash':'fas fa-eye']" id='eye' @click='click2' ></i>
                    </div>          
                </div>
                <div class="field">
                    <input class='check-box' required type='checkbox' v-model='accept'>
                    <span @click='goPolicy()' class='check-box-text'>・利用規約に同意します。</span>
                </div>
                <div class='error-form' v-if='passwordError||passwordError2||mailError||nameError||mailInUseError'>
                    <i class="fas fa-exclamation-triangle"></i>
                    <div v-if='mailError'>{{ mailError}}</div>
                    <div v-if='nameError'>{{ nameError }}</div>
                    <div v-if='mailInUseError'>{{ mailInUseError }}</div>
                    <div v-if='passwordError' >{{ passwordError }}</div> 
                    <div v-if='passwordError2'>{{ passwordError2 }}</div> 
                </div>    
                <!-- <p class='password-text'>{{ accept }}</p> -->
                <div>
                    <button class='fbottun' ref='bform'>次へ</button>
                </div>
            </div>
        </form>
    </div>
</template>

<script>
export default {
    data(){
        return{
            username:this.$store.state.signup.username,
            country:this.$store.state.signup.country,
            viewCountry: this.viewableCountry,
            password:this.$store.state.signup.password,
            email:this.$store.state.signup.email,
            password2:'',
            accept:'',
            showButton:true,
            passwordError:'',
            passwordError2:'',
            mailInUseError:null,
            nameError:false,
            mailError:false,
            passType:false,
            passType2:false,
            showSellect:false
            
        }
    },
    props:[
        'showProgress',
        'viewableCountry',
        'countryData'
    ],
    mounted(){
        this.progressHandle()
        console.log(this.showProgress)
    },
    updated(){
        // this.getFilledItems(event.target.value)
        this.showButtonHandler()
        // console.log(this.showButton,this.username,event.target.value)
    },
    computed: {
        inputType: function () {
        return this.passType ? "text" : "password";
        },
        inputType2: function () {
        return this.passType2 ? "text" : "password";
        }
    },
    watch:{
        showButton:function(v) {if (v == false) { this.$refs.bform.classList.add('button-hover')}
        else{this.$refs.bform.classList.remove('button-hover')}},
    },
    methods:{
        // getFilledItems(item){
        //     console.log('filled')
        //     if(item == 'Username'){
        //         this.username = item
        //         }
        //     if(item == 'Country'){
        //         this.country = item
        //     }
        //     if(item == 'password'){
        //         this.password = item
        //     }
        // },
        progressHandle(){
            if(this.showProgress == true){
            this.$emit('handle')
            }
        },
        click(){
            this.passType = !this.passType
        },
        click2(){
            this.passType2 = !this.passType2
        },
        showButtonHandler(){
            if(this.password!=''&&this.password2!=''&&this.accept==true
                &&this.username!=''
                // &&this.country!=''
                ){
                this.showButton = false
                }
            else{
                this.showButton = true
                }
            },
        async submitForm(){
            // validate password
            console.log('clicked',this.password,this.password2)
            this.passwordError = this.password == this.password2?
            '' : '@passwords are not the same'
            console.log(this.passwordError)
            this.passwordError2 = this.password.length > 7?
            '' : '@password is less than 8 char'
            this.nameError = this.username.length < 21 ?
            '' : '@name must be less than 20 chars'
            await this.$store.dispatch('checkEmail',this.email)
                this.mailInUseError = this.$store.state.signup.checkedEmail ?
                '' : '@address is already in use'
            console.log('nameerror:',this.nameError,'mailerror',this.mailError,this.passwordError)
                if (this.passwordError == ''&&this.passwordError2 == ''&&this.$store.state.signup.checkedEmail == true&&
                    this.nameError == ''&& this.mailError ==''){
                    console.log('in second if',this.passwordError,this.passwordError2,this.$store.state.signup.checkedEmail)
                    this.$emit('edithandle')
                    this.$store.commit('getPassword',this.password)
                    this.$store.commit('getUsername',this.username)
                    this.$store.commit('getEmail',this.email)
                    this.$store.commit('getEmail2',this.email2)
                    this.$store.commit('getCountry',this.country)
            }
        },
        showSelectionTrue(){
            this.showSellect = true
            // this.$store.commit('showModalTrue')
            this.$store.commit('fixedScrollTrue')
        },
        showSelectionFalse(){
            this.showSellect = false
            // this.$store.commit('showModalFalse')
            this.$store.commit('fixedScrollFalse')
        },
        addCountry(country){
            this.country = this.convertCountryToTwoCode(country)
            this.viewCountry = country
            this.$emit('setCountryForEdit',country)
            console.log('check',this.viewCountry,this.country)
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
        goPolicy(){
            window.open('/terms-and-conditions/', '_blank');
        }
    },        
}
</script>

<style scoped lang='scss'>
@import "style/_variables.scss";
.password-wrapper{
    width:100%;
    height: 100vh;
    flex-direction: column;
    display: flex;
    // padding-top:5rem;
    // justify-content: center;
    align-items: center;

}
    .id-form{
        margin-bottom: 100px;
        width:100vw;
        }
    .password-text{
        color:white;
        font-size:1.2rem;
        font-weight: bold;
        margin-bottom: 1.5rem;
       
    }
    .field-wrapper{
        flex-direction: column;
        align-items: flex-start;;
        display: flex;
        align-items: center;
        margin-top:1.5rem;
        .error-form{
            width: 17rem;
        }
    }
    .field{
        display: flex;
        justify-content: flex-start;
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
    input[type="password"]:focus {
        outline: none;
        }
        .input-box:focus-within{
        border: solid $base-color;
        
        }
    input[type="text"]:focus {
        outline: none;
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
    .text-box{
        width: 14rem;
        border:none;
        background: $back-white;
        margin-left:0.5rem;
        position:absolute;
        left:1rem;
    }
    .select-box{
        width: 45%;
        border:none;
        background: $back-white;
        // margin-left:0.5rem;
    }
    .select-dammy-box{
        caret-color: transparent;
        margin-left: 1rem;
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
    .check-box-text{
        color:white;
        cursor: pointer;
    }
    .error-wwapper{
        position:relative;
    }
    .error-wrapper{
        position:absolute;
        width: 100%;
        height:5rem;
    }
    .error{
        color:red;
        text-align: center;
        font-weight: bold;
        margin-bottom:0.2rem;
        border: 0.1rem solid red;
        background:rgb(243, 214, 214);
        width: 100%;
        height:60%;
        margin-top:1rem;
        // margin-left: auto;

        // margin-right: 0;
        }
    p {
        color:white;
    }
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
            color: $dark-blue;
            margin-top: 1.5rem;
            padding-bottom: 1rem;
        }
        .addedCountry{
                // background: red;
                color: black;
                margin-bottom: 0.5rem;
                font-weight: bold;
                background: rgba(162, 161, 161, 0.3);
            }
        .each-country{
            color: black;
            font-size: 0.8rem;
            margin-top: 0.3rem;
            margin-bottom: 0.3rem;
            transition: .5s;
            .country-name{
                color: black;
            }
        }
        .each-country:hover{
            background: $lite-gray;
            
        }
    }
}
</style>