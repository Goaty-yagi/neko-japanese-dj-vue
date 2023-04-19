<template>
    <div id="wrapper">
        <Header
        id="header"/>
        <div :class="{'app-laoding-center':$store.state.isLoading||!mounted}">
          <div class="is-loading-bar has-text-centered" v-bind:class="{'is-loading': $store.state.isLoading||!mounted}">
            <div class="lds-dual-ring"></div>
          </div>
        </div>
        <ConnectionError
        id="connection-error"
        v-if="$store.state.signup.apiError.any"
        />
        <section class="main-section" v-if="mounted">
          <!-- <div class="is-loading-bar has-text-centered" v-bind:class="{'is-loading': !mounted }">
              <div class="lds-dual-ring"></div>
          </div> -->
            <router-view
            id='router'/>
            <!-- <Footer
            id="footer"
            :class="{'custom-footer':$store.getters.fixedScroll}"
            v-if="!$store.state.isLoading&&!$store.state.quiz.onQuiz&&!$store.getters.onSigningup&&!$store.getters.showModal&&componentMounted"/> -->
            
        </section>
        <Footer
            v-if='!$store.state.isLoading&&mounted'
            id="footer"
           />
        <div class='mobile-header'
        v-if="!$store.state.quiz.onQuiz">
            <MobileHeader
            v-if="!$store.state.signup.apiError.any"/>
        </div>
    </div>
</template>

<script>
import Footer from '@/components/html_components/Footer.vue'
import Header from '@/components/html_components/Header.vue'
import MobileHeader from '@/components/html_components/MobileHeader.vue'
import ConnectionError from '@/views/not-found/ConnectionError.vue'
import Sent from '@/components/signin/Sent.vue'
import { computed, ref } from 'vue'
import { useStore } from 'vuex'
import { router } from "./main.js"

export default{
  setup(){
    const store = useStore()
    return{
      user: computed(() => store.state.signup.user),
      djangoUser: computed(() => store.state.signup.djangoUser),
      email: computed(() => store.state.signup.email),
      password: computed(() => store.state.signup.password),
      emailVerified: computed(() => store.state.signup.emailVerified),
      mounted: computed(() => store.state.signup.mounted),
      authIsReady: computed(() => store.state.signup.authIsReady),
    }
  },
  data(){
    return{
      quizurl:'/quiz/2',
      showSent:false,
    }
  },
  components: {
    Footer,
    Sent,
    Header,
    MobileHeader,
    ConnectionError
  },
  created() {
    this.setMetaElement()
    console.log("CREATE")

  },
  mounted(){
    console.log(this.mounted, document.location.origin)
    console.dir(document)
  },
  watch: {
    $route(to){
      document.title = 'Neko-Japanese-' + to.name
    }
  },
  methods:{
    storeReset(){
          this.$store.commit('reset')
    },
    setMetaElement() {
      const origin = document.location.origin
      const metaElement = document.createElement('meta')
      metaElement.setAttribute('property', "og:url")
      metaElement.setAttribute('content', origin)
      document.head.appendChild(metaElement)
    },
  async resent(){
        // try{
            await this.$store.dispatch('sendEmailVerify')
            this.handleShowSent()
    },
    handleShowSent(){
      this.showsent = true
    },
  }
}
</script>


<style lang="scss">
@import '../node_modules/bulma';
@import "style/_variables.scss";
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  background: linear-gradient(#5B759F,#1C254C);
  min-height: 100vh;
}
 .wrapper2{
   position:absolute;

}
#header{
}
.app-laoding-center {
   position: fixed;
    inset: 0;
    margin: auto;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
#router{
  min-height: 80vh;
}
#footer{
}
.custom-footer{
  z-index: -1;
}
#connection-error{
  height: 100vh;
}
.main-header{
  position:relative;
  bottom:0;
}
.main-section{
  // min-height: 100vh;
  // width: 100vw;

}

.lds-dual-ring {
  display: inline-block;
  width: 80px;
  height: 80px;
}
.lds-dual-ring:after {
  content: " ";
  display: block;
  width: 64px;
  height: 64px;
  margin: 8px;
  border-radius: 50%;
  border: 6px solid rgb(214, 9, 9);
  border-color: #ccc transparent #ccc transparent;
  animation: lds-dual-ring 1.2s linear infinite;
}
@keyframes lds-dual-ring {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.is-loading-bar {
  height: 0;
  overflow: hidden;

  -webkit-transition: all 0.3s;
  transition: all 0.3s;

  &.is-loading {
    height: 80px;
  }
}    
  // here intend to be pablic css
  
  #color-button{
    background: linear-gradient($base-lite,$base-color);
    color:white;
    border: 0.1rem solid  $base-color;
    transition:0.3s;
  }
  #color-button:hover{
    background: $base-color;
    color:white;
    font-weight: bold;
    border: 0.1rem solid  darken($base-color,10%);
  }
  // form button
  .fbottun{
        margin-top:1rem;
        border-radius: 100vh;
        border: 2px solid $base-color;
        margin:1rem;
        padding-top:0.3rem;
        padding-bottom:0.3rem;
        padding-left:1rem;
        padding-right:1rem;        
        background: transparent;
        color: white;
        font-size: 1rem;
        transition:0.5s;
    }
    .fbottun.button-hover{
        background: $base-color;
        color:white;
        font-weight:bold;
        border: 2px solid darken($base-color,10%);
    }
    .fbottun.button-hover:hover{
        background: transparent;
        color:$base-color;
    }
    // formerror
    .error-form{
        color:red;
        text-align: center;
        font-weight: bold;
        margin-bottom:0.2rem;
        border: 0.2rem solid red;
        border-radius: 1rem;
        background:rgb(252, 252, 252);
        width: 100%;
        padding-top:0.5rem;
        padding-bottom:0.5rem;
        transition:0.5s;
        align-self: center;
      }
      .form-error{
        border: solid red;
      }
@media(min-width: 630px){
  .mobile-header{
    display:none;
  }
  .wrapper{
    position:relative
  }
}
// animation for name'notice'
.notice-enter-from{
    opacity: 0;
  }
  .notice-enter-to{
    opacity: 1 ;
  }
  .notice-enter-active, .notice-leave-active {
  transition: opacity .5s;
  }
</style>
