<template>
    <div class="header-wrapper">
        <div v-if='authIsReady'>
            <nav class="nav-container">
                <div class="nav-brand">
                    <router-link @click="storeReset" to="/" >
                        <img src="@/assets/logo.png">
                    </router-link>
                </div>
                <div class="handle-show">
                    <div class='nav-menu-flex'>
                        <div class="nav-menu" @click="showMobileMenu =false">
                            <router-link :to="{ name: 'Home'}" @click="storeReset" class="nav-item"><i class="fas fa-home" ></i>Home</router-link>
                            <router-link v-if='user' :to="{ name: 'QuizHome'}" class="nav-item "><i class="fas fa-lightbulb"></i>Quiz</router-link>
                            <router-link :to="{ name: 'Community'}"  class="nav-item"><i class="far fa-comments fas"></i>Community</router-link>
                            <router-link v-if='!user' :to="{ name: 'Login'}" class="nav-item"><i class="fas fa-sign-in-alt"></i>Login</router-link>
                            <router-link v-if='!user' :to="{ name: 'Signup'}" class="nav-item signup"><i class="fas fa-user-plus"></i>Signup</router-link>
                            <router-link v-if='user' :to="{ name: 'Account'}" class="nav-item"><i class="fas fa-robot"></i>Account</router-link>
                            <router-link v-if='isStaff' :to="{ name: 'Dboard'}" class="nav-item"><i class="fas fa-chart-bar"></i>Dashboard</router-link>
                            <div v-if='user' class="nav-item last" ><i class="fas fa-sign-out-alt"></i>Logout
                                <Popover
                                class='pop'
                                    :popoverConfig='popoverConfig'
                                    />
                            </div>
                        </div>
                    </div>
                </div>     
            </nav>
        </div>
    </div>
</template>

<script>
import {router} from "@/main.js"
import { computed } from 'vue'
import { useStore } from 'vuex'
import  Popover from '@/components/parts/Popover.vue'
export default {
    components: {
        Popover
    },
  setup(){
    const store = useStore()
    return{
      user: computed(() => store.state.signup.user),
      emailVerified: computed(() => store.state.signup.emailVerified),
      authIsReady: computed(() => store.state.signup.authIsReady),
      isStaff: computed(() => store.state.signup.user?store.state.signup.user.is_staff:false)
    }
  },
    data(){
        return{
            showMobileMenu: false,
            handleWidthAndHeight:false,
            showBrand:true,
            width:'',
            Height:'',
            popoverConfig:{
                mainText:'ログアウトしますか。',
                cancelFun: this.showPopoverHandler,
                confirmFun: this.logout,
                cancelText:'戻る',
                confirmText:'ログアウト'
            }
        }
    },
    computed:{
    },
    mounted(){
    },
    beforeUnmount(){ 
    },
    methods:{
    storeReset(){
          this.$store.commit('reset')
    },
    getAccount(id){
        router.push(`/account/${id}` )
    },
    // showPopoverHandler() {
    //     console.dir(this.$refs.popover)
    //     this.$refs.popover.showPopoverHandler()

    // },
    async logout(){
        console.log("LOGAOUT_CLICKED")
      await this.$store.dispatch('logout')
    },
  }
}
</script>

<style scoped lang="scss">
@import "style/_variables.scss";
.header-wrapper{
    width: 100vh; 
    padding-top: 1rem;
    .nav-container{
        position: relative;
        display: flex;
        justify-content: flex-end;
        width: 100%;
        img{
            position: absolute;
            width: 3rem;
            height: 3rem;
            left:0;
            top:0;
        }
        .nav-menu-flex{
            display: flex;
            justify-content: flex-end;
            align-items: center;
            padding:1rem;
            width: 100%;
            .nav-menu{
                margin-top: 1.5rem;
                margin-right: 1rem;
                display: flex;
                .fas{
                    margin-right: 0.5rem;
                }
                .nav-item{
                    position: relative;
                    color:white;
                    border-right: 0.2rem solid $base-color;
                    padding-right: 1rem;
                    padding-left: 1rem;
                    padding-top: 0.5rem;
                    padding-bottom: 0.5rem;
                    transition: 0.5s;
                }
                .signup{
                    border: solid $base-white;
                    color: rgb(240, 205, 4);
                    margin-left: 0.5rem;
                    padding-right: 1rem;
                    padding-left: 0.5rem;
                    padding-top: 0.5rem;
                    padding-bottom: 0.5rem;
                    
                }
                .last{
                    border-right: none;
                    position: relative;
                }
                .nav-item:not(.pop):hover{
                    color:gray;
                    background: $base-white;
                    box-sizing: inherit;
                }
                .signup:hover{
                    border: solid $dark-blue;
                    color: $dark-blue;
                }
                .auth{
                    display: flex;
                    flex-basis: 40%;
                    margin-left: 0.5rem;
                    margin-right: 0.5rem;
                    .nav-auth-item{
                        color:white;
                        flex-basis: 50%;
                        margin-left: 0.5rem;
                        margin-right: 0.5rem;
                        padding: 0.3rem;
                        transition: 0.5s;
                        cursor : pointer;
                        border: solid rgba(0, 0, 0, 0);
                    }
                    .nav-auth-item:hover{
                        color:gray;
                        border: solid gray;
                        box-sizing: inherit;
                    }
                }
            }
        }
    }    
}
@media(min-width: 630px)and(max-width: 660px){
    .nav-brand{
        display: none;
    }
}
@media(max-width: 629px){
    .header-wrapper{
        height: 50px
    }
    .handle-show{
        display: none;
    }
}

  .header-wrapper{
    width:100vw;

  }
  .navbar {
    &.is-transparent {
      background-color: transparent;
      background-image: none;
      }
    }
  .navbar-end{
    color:white;
  }
</style>