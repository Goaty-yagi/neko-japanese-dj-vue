<template>
  <div class="abstract-wrapper">
    <div v-if="!toast" class="l-wrapper">
      <div class="l-container confirm">
        <div v-if="!clicked" class="unclicked">
          <p class="confirm-header">{{ mainText }}</p>
          <div
            class="each-container"
            v-for="(val, key, index) in formObj"
            v-bind:key="index"
          >
            <p class="each-title">{{ key }}</p>
            <p class="space">:</p>
            <p class="content">{{ val }}</p>
          </div>
          <div
            class="text-container"
            v-for="(val, key, index) in formTextareaObj"
            v-bind:key="index"
          >
            <p class="text-title">{{ key }}</p>
            <p class="text-content">{{ val }}</p>
          </div>
          <div v-if="image">
            <img :src="image" />
          </div>
          <div class='confirm-note-wrapper' v-if='noteText'>
            <i class="fas fa-exclamation-triangle"></i>
            <p v-if='noteText' class="confirm-note-text">{{ noteText }}</p>
          </div>
          <div v-if="checkedPropsExist(showButton)" class="button-container">
            <div v-if="checkedPropsExist(showCalcelButton)" @click="cancelFunction">キャンセル</div>
            <div @click="buttonFunction">{{ buttontext }}</div>
          </div>
        </div>
        <div v-if="clicked && afterClickObj.type === 'modal'" class="clicked">
          <p class="confirm-header">{{ afterClickObj.title }}</p>
          <p>{{ afterClickObj.text }}</p>
          <div class="button-container">
            <div @click="afterClickObj.buttonFunc()">
              {{ afterClickObj.buttonText }}
            </div>
          </div>
        </div>
      </div>
      <div></div>
    </div>
    <div
      v-if="clicked && afterClickObj.type === 'toast'"
      class="notification-blue"
    >
      <p class="notification-text">{{ afterClickObj.text }}</p>
    </div>
  </div>
</template>

<script>
export default {
  props: [
    "mainText",
    "noteText",
    "formObj",
    "formTextareaObj",
    "image",
    "showButton",
    "buttontext",
    "buttonFun",
    "cancelFun",
    "showCalcelButton",
    "afterClickObj", //include type,title text,buttonText, buttonFunc type should be 'modal' or'toast'
  ],
  data() {
    return {
      clicked: false,
      toast:false,
      top:0
    };
  },
  computed: {
    checkAfterClickType() {},
    // checkedShowButton() {
    //   if(typeof this.showButton !== 'undefined') {
    //     console.log("SB",this.showButton, this.showButton!== 'undefined')
    //     return this.showButton
    //   } else {
    //     return true
    //   }
    // },
    // checkedShowCancelButton() {
    //   if(typeof this.showButton !== 'undefined') {
    //     console.log("SB",this.showButton, this.showButton!== 'undefined')
    //     return this.showButton
    //   } else {
    //     return true
    //   }
    // }
  },
  mounted() {
    console.log("mounted",window.scrollY, 'docu',this.formObj);
    this.top = window.scrollY
    document.body.style.top = `-${window.scrollY}px`;
    document.body.style.position = 'fixed'
    this.$emit("handle");
  },
  beforeUnmount() {
    document.body.style.position = ''
    window.scrollTo(0, this.top)
  },
  methods: {
    checkedPropsExist(prop) { //for boolean only 
      if(typeof prop !== 'undefined') {
        return prop
      } else {
        return true // default true
      }
    },
    cancelFunction() {
      this.$emit("cancelFun");
    },
    async buttonFunction() {
      if(typeof this.afterClickObj !== 'undefined') {
        if (this.afterClickObj.type === "modal") {
        this.$emit("buttonFun");
        this.clicked = true;
        } else {
          await this.$emit("buttonFun");
          this.clicked = true;
          this.toast = true
          setTimeout(() => {
            this.afterClickObj.afterCreatedFunc();
          }, 3000);
        }
      } else {
        this.$emit("buttonFun");
      }
    },
  },
};
</script>

<style scoped lang='scss'>
@import "style/_variables.scss";
.abstract-wrapper {
    position: absolute;
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
}
.l-container {
  padding: 1rem;
  font-weight: bold;
  .created-header {
    color: $dull-red;
    margin-bottom: 1rem;
  }
}
.each-container {
  width: 100%;
  display: flex;
  justify-content: center;
  .each-title {
    flex-basis: 45%;
    width: 50%;
    display: flex;
    justify-content: flex-end;
  }
  .space {
    flex-basis: 5%;
  }
  .content {
    flex-basis: 45%;
    width: 45%;
    display: flex;
  }
}
.button-container {
  width: 100%;
  display: flex;
  justify-content: center;
  margin-top: 2rem;
  div {
    margin: 0 0.5rem;
    border: solid gray;
    padding: 0.2rem 0.5rem;
    transition: 0.5s;
    font-weight: bold;
  }
  div:hover {
    color: gray;
  }
}
.confirm {
  padding: 1rem;
  .confirm-header {
    font-size: 1.3rem;
    margin: 1rem 0;
    color: $dull-red;
    white-space: pre-wrap;
  }
  p {
    margin-bottom: 1rem;
    font-weight: bold;
    font-size: 0.9rem;
  }
  .each-container {
    width: 100%;
    display: flex;
    justify-content: center;
    .each-title {
      flex-basis: 45%;
      width: 50%;
      display: flex;
      justify-content: flex-end;
    }
    .space {
      flex-basis: 5%;
    }
    .content {
      flex-basis: 45%;
      width: 45%;
      display: flex;
    }
  }
  .button-container {
    width: 100%;
    display: flex;
    justify-content: center;
    div {
      margin: 0 0.5rem;
      border: solid gray;
      padding: 0.2rem 0.5rem;
      transition: 0.5s;
      font-weight: bold;
    }
    div:hover {
      color: gray;
    }
  }
  .text-container {
    width: 100%;
    display: flex;
    align-items: center;
    flex-direction: column;
    .text-content {
      white-space: pre-wrap;
      background: $lite-gray;
      padding:0.5rem;
      width: 80%;
    }
  }
}
.confirm-note-wrapper{
  color: $dull-red;
  padding-top: 0.5rem;
  border: thick double red;
}
</style>