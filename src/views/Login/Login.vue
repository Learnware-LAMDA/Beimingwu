<template>
    <div class="fill-height">
        <div class="fill-height flex flex-row justify-center">
            <v-col class="flex flex-column justify-center items-center" cols="12" md="6">
                <v-card class="mx-auto w-1/1 p-4 elevation-20" max-width="500">
                    <v-card-title>
                        <h1 class="text-lg-h4 text-h5 m-2">Login</h1>
                    </v-card-title>
                    <v-card-text>
                        <v-form ref="form" v-model="valid" lazy-validation>
                            <v-text-field
                                v-model="email"
                                :rules="emailRules"
                                label="E-mail"
                                required
                            ></v-text-field>
                            <v-text-field
                                v-model="password"
                                :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                                :rules="passwordRules"
                                :type="showPassword ? 'text' : 'password'"
                                label="Password"
                                required
                                @click:append="showPassword = !showPassword"
                            ></v-text-field>                     
                        </v-form>
                    </v-card-text>
                    <v-card-actions>
                        <v-btn block class="bg-primary py-5" color="white" @click="login">Login</v-btn>
                    </v-card-actions>
                    <v-card-actions>
                        Don't have an account?
                        <v-spacer></v-spacer>
                        <v-btn variant="text" color="primary" @click="register">Register first</v-btn>
                    </v-card-actions>
                </v-card>
            </v-col>
        </div>
    </div>
</template>