<template>
    <div class="signup">
        <div class="hero">
            <div class="hero-body has-text-centered">
                <h1 class="title">Sign up</h1>
            </div>
        </div>
    
        <section class="section">
            <div class="container">
                <div class="columns">
                    <div class="column is-4 is-offset-4">
                        <form action="">
                            <div class="field">
                                <label for="">Email</label>
                                <div class="control">
                                    <input type="email" class="input"/>
                                </div>
                            </div>

                            <div class="field">
                                <label for="">Password</label>
                                <div class="control">
                                    <input type="password" class="input"/>
                                </div>
                            </div>

                            <div class="field">
                                <label for="">Repeat password</label>
                                <div class="control">
                                    <input type="password" class="input"/>
                                </div>
                            </div>

                            <div class="field">
                                <div class="control">
                                    <button class="button" style="background: #163820; color: #ffffff;">Sign up</button>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </section>
    </div>
</template>

<script>
export default {
  name: 'SignUp'
}
</script>
