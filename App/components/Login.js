import React, { Component } from 'react';
import { Text, View, StyleSheet, TouchableOpacity, Image } from 'react-native';
import Icon from 'react-native-vector-icons/FontAwesome';
import { Input } from 'react-native-elements';
import Dialog, { DialogContent, DialogFooter, DialogButton } from 'react-native-popup-dialog';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default class Login extends Component {
    constructor(props){
        super(props);
        this.getData()
        this.state = {
            name: '',
            password: '',
            idPlayer: '',
            visible: false,
            visible2: false,
            visible3: false,
            visible4: false,
        };
    }

    onSubmit = async () =>{
        try{
            await AsyncStorage.setItem('name', this.state.name)
            await AsyncStorage.setItem('password', this.state.password)
        } catch (err){
            console.log(err)
        }
    }

    getData = async () =>{
        try{
            const name = await AsyncStorage.getItem('name')
            const password = await AsyncStorage.getItem('password')
            if(name != null && password != null){
                this.setState({name})
                this.setState({password})
                this.Log_in()
            } else {
                this.setState({visible2: true})
            }
        } catch (err){
            console.log(err)
        }
    }

    Log_in = async () =>{
        try{
            const response = await fetch('http://192.168.100.4:5050/login',{
                method: 'POST',
                headers: {
                    Accept: 'application/json',
                    'content-type':'application/json'
                },
                body: JSON.stringify({
                    name:this.state.name,
                    password:this.state.password,
                })
            });
            const resp = await response.json();
            console.log(resp.Response);
            if(resp.Response != "-1"){
                this.onSubmit();
                this.setState({idPlayer: resp.Response});
                this.setState({visible2: true})
                return this.props.navigation.navigate("Última Puntuación", {id: this.state.idPlayer})
            } else {
                this.setState({visible: true})
            }
        } catch (error) {
            console.error(error);
        }
    };

    Sign_in = async () =>{
        try{
            const response = await fetch('http://192.168.100.4:5050/signin',{
                method: 'POST',
                headers: {
                    Accept: 'application/json',
                    'content-type':'application/json'
                },
                body: JSON.stringify({
                    name:this.state.name,
                    password:this.state.password,
                })
            });
            const resp = await response.json();
            console.log(resp.Response);
            if(resp.Response != "-1"){
                this.setState({visible3: true})
            } else {
                this.setState({visible4: true})
            }
        } catch (error) {
            console.error(error);
        }
    };

    render() {
        return (
            <View>
                <Image 
                style={{width: 300, margin: 35, marginTop: -50}}
                resizeMode="contain"
                source={require('./Logo.png')} />
                {this.state.visible2?
                <View>
                <View style = {{width: 315, marginTop: -80, marginLeft: 20}}>
                    <Input
                    placeholder='Nombre de usuario'
                    placeholderTextColor='#b0e0e6'
                    color = '#f0ffff'
                    inputContainerStyle={{borderBottomColor: "#b0e0e6"}}
                    value = {this.state.name}
                    leftIcon={<Icon name='user' size={24} color='#f0fff0'/>}
                    onChangeText={name=>this.setState({name})}
                    />
                </View>

                <View style = {{width: 315, marginTop: 15, marginLeft: 20}}>
                    <Input
                    placeholder='Contraseña'
                    placeholderTextColor='#b0e0e6'
                    color = '#f0ffff'
                    inputContainerStyle={{borderBottomColor: "#b0e0e6"}}
                    value = {this.state.password}
                    leftIcon={<Icon name='lock' size={24} color='#f0fff0'/>}
                    secureTextEntry = {true}
                    onChangeText={password=>this.setState({password})}
                    />
                </View>

                <View style={styles.boton} >
                    <TouchableOpacity onPress={this.Log_in}>
                        <Icon name="sign-in" size={16} color="#f0ffff" style={{height: 20, textAlignVertical: 'center'}}>
                            <Text style={{fontSize: 16}}>  Iniciar Sesión</Text>
                        </Icon>
                    </TouchableOpacity>
                </View>

                <Dialog
                    visible={this.state.visible}
                    footer={
                    <DialogFooter>
                        <DialogButton
                        text="OK"
                        onPress={() => {
                           this.setState({ visible: false });
                        }}
                        />
                    </DialogFooter>
                    }
                >
                    <DialogContent>
                        <Text style={{fontSize: 18, marginTop: 20, textAlign: 'center',}}>Nombre de usuario o contraseña incorrectos</Text>
                    </DialogContent>
                </Dialog>

                <Dialog
                    visible={this.state.visible3}
                    footer={
                    <DialogFooter>
                        <DialogButton
                        text="OK"
                        onPress={() => {
                           this.setState({ visible3: false });
                        }}
                        />
                    </DialogFooter>
                    }
                >
                    <DialogContent>
                        <Text style={{fontSize: 18, marginTop: 20, textAlign: 'center',}}>Usuaio creado correctamente.</Text>
                    </DialogContent>
                </Dialog>

                <Dialog
                    visible={this.state.visible4}
                    footer={
                    <DialogFooter>
                        <DialogButton
                        text="OK"
                        onPress={() => {
                           this.setState({ visible4: false });
                        }}
                        />
                    </DialogFooter>
                    }
                >
                    <DialogContent>
                        <Text style={{fontSize: 18, marginTop: 20, textAlign: 'center',}}>Este usuario ya existe.</Text>
                    </DialogContent>
                </Dialog>

                <View style={styles.boton} >
                    <TouchableOpacity onPress={this.Sign_in}>
                        <Icon name="user-plus" size={16} color="#f0ffff" style={{height: 20, textAlignVertical: 'center'}}>
                            <Text style={{fontSize: 16}}>  Crear Cuenta</Text>
                        </Icon>
                    </TouchableOpacity>
                </View>
                </View>
                :null}
            </View>
        )
    }
}

const styles = StyleSheet.create({
    boton: {
        borderWidth: 3, 
        borderRadius: 6,
        borderColor: '#00ced1',
        marginLeft: 110, 
        marginTop: 25,
        marginBottom: 10, 
        width: 150,
        alignItems: 'center',
        backgroundColor: '#008b8b',
        padding: 10,
    }
})