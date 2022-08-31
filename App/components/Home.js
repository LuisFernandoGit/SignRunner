import React, { Component } from 'react';
import { Text, View, FlatList, StyleSheet } from 'react-native';
import { Card, FAB, Button } from 'react-native-paper'
import {Picker} from '@react-native-picker/picker'

export default class Home extends Component {
    constructor(props) {
      super(props);
  
      this.state = {
        last: 0,
        lastTen: [],
        difficulty: 'n',
        id: '1'
      };
    }

    async getScores() {
        try{
            //Replace "0.0.0.0" for your local ip (shown in the api.py console).
            const response = await fetch('http://0.0.0.0:5050/promedio/'+this.state.difficulty+'/'+this.state.id);
            const article = await response.json();
            this.setState({lastScore: article.last})
            this.setState({lastTen: article.last_ten})
            console.log(this.state.lastScore)
            console.log(this.state.lastTen)
        } catch (error) {
            console.error(error);
        }
    };
  
    componentDidMount() {
        this.getScores();
    }
  
    render() {
        const data2 = [
            {id: 1, title: "First Title", body: "First Body"},
            {id: 2, title: "Second Title", body: "Second Body"},
            {id: 3, title: "Third Title", body: "Third Body"}
        ]
    
        const renderData = (item) => {
            return(
                <Card style = {styles.cardStyle}>
                    <Text style = {{fontSize: 20}}>{item}</Text>
                </Card>
            )
        }
      
        return (
            
            <View style = {{flex: 1}}>
                <View>
                    <Text style={{fontSize:22, marginLeft:30, marginTop:20}}>Dificultad</Text>
                    <View style={{borderColor: '#778899', borderBottomWidth: 1, width: 230, marginLeft: 30, marginBottom: 20}}>
                        <Picker
                        onValueChange={(difficulty)=>this.setState({difficulty})}
                        selectedValue = {this.state.difficulty}
                        style={styles.picker}
                        >
                            <Picker.Item label = "Fácil" value = "e" style={{fontSize:18}}/>
                            <Picker.Item label = "Normal" value = "n" style={{fontSize:18}}/>
                            <Picker.Item label = "Difícil" value = "h" style={{fontSize:18}}/>
                        </Picker>
                    </View>
                </View>

                <Button
                    style = {{margin:10}}
                    icon = 'pencil'
                    mode = 'contained'
                    onPress={() => this.getScores()}
                    >Actualizar Puntajes</Button>
                <View style = {styles.spliters}>
                    <Text style = {{fontSize: 22}}>Último Puntaje:</Text>
                </View>
                <Card style = {styles.cardStyle}>
                    <Text style = {{fontSize: 20}}>{this.state.lastScore}</Text>
                </Card>
                <View style = {styles.spliters}>
                    <Text style = {{fontSize: 22}}>Puntajes Recientes:</Text>
                </View>
                <FlatList
                data={this.state.lastTen}
                renderItem={({item})=>{
                    return renderData(item)
                }}
                //keyExtractor={item => item.id}
                />
                <FAB
                style = {styles.fab}
                small = {false}
                icon = "plus"
                theme = {{colors: {accent: "green"}}}
                onPress={() => console.log("presionado")}
                //onPress = {() => this.props.navigation.navigate("Create")}
                />
            </View>
        );
    }
};

const styles = StyleSheet.create({
    cardStyle: {
        margin: 10,
        padding: 10
    },
    fab: {
        position: 'absolute',
        margin: 16,
        right: 0,
        bottom: 0
    },
    spliters: {
        margin: 10,
        borderBottomWidth: 2,
    }
});

//export default Home;