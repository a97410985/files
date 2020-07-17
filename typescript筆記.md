## js物件

## null和undefined的比較

1. undefined的緣由(跟c++做比較)變數一定會需要有個初始值，就c++而言如果變數宣告時沒有初始化，像是一個整數變數，那麼他的值會是亂數(就看使用的記憶體空間原本放什麼)，剛才的是c++的作法，至於javascript的做法就是宣告了一個變數，如果宣告時沒有賦值會自動給一個undefined的值
2. null的緣由(跟c++做比較)，null的概念在c++有，跟pointer相關，就是讓指標可以指向一個空的地方，像是link list最尾端的節點的nextPtr*會指向null，因為後面沒東西，javascript也會有類似的東西，不過null可以給primitive變數(string、number、...)和物件參考用，概念也是差不多，有時候變數或物件參考會是空的，並不是沒有初始化。至於物件參考被賦予null會影響到物件使用的資源釋放，像是所有某個物件的參考都被設為null，javascript的垃圾回收機制就會回收掉那個物件。

## 函數 

1. `function`在javascript中具備怎樣的地位，與`c++`做比較。(`比較不同處，有哪些新的東西`)
   function在javascript是first-class object，可以作為參數傳入、作為回傳值回傳，簡單來說就是被當作一般的物件使用(有屬性和方法)，像是函數可能會有一個參數是callback函數，當函數執行完的時候會呼叫callback函數，畢竟瀏覽器會有很多獲取資源(需要時間)或許多事件相關的東西(需要綁一個函數作為觸發，`addEventListener`)。c++很顯然函數不能作為參數和回傳值，c++就只有一般primitive變數和指標可以。

   1. 因為`function`是first-class object，所以可以被當作一般物件

      1. 一般的物件可以用`賦值運算子=`給某個變數參考，所以javascript的function也可以

         一般javascript物件

         ```typescript
         let a = {dog: "bark", cat: "meow"}
         ```

         一般javascript函數

         ```typescript
         let greet2 = function(name: string) {
           return 'hello ' + name
         }
         ```

      2. 有專門建構函數的constructor

         javascript某些builit-in object~Array有建構子可以建立一個array

         ```typescript
         let fruits = new Array(2) // 建立一個陣列有兩個元素
         ```

         javascript的函數也有

         ```typescript
         let greet5 = new function('name', 'return "hello " + name')
         ```

2. function的特殊語法，跟lambda函數式程式語言有關，像是arrow function(匿名函數+有時候會需要只會出現一次的函數)

   ```typescript
   (參數1, 參數2, ...) => { 函數body } // 沒有函數名稱!!!
   ```

   ```typescript
   let greet3 = (name: string) => {
       return 'hello ' + name
   }
   ```

   如果函數body只有一行可以把`{}`拿掉

   ```typescript
   let greet4 = (name: string) => 'hello ' + name
   ```

3. 參數

   1. 能有些參數可以也可以沒有 ~ optional parameters

      關鍵符號 : `?`，問號的意思就是可能有也可能沒有，跟regular expression的`?`功能是一樣的，像是下面第二個參數可有可沒有

      注意事項: 要放在一般參數的後面

      ```typescript
      function log(msg1: string, msg2?: string) {
        console.log(msg1);
        if (msg2) console.log(msg2);
      }
      // haha
      log("haha");
      // dog
      // cat
      log("dog", "cat");
      
      ```

      語法

      ```typescript
      (arg1, arg2?: type) // arg2是optional parameter
      ```

   2. 有些參數在沒有指定值的時候會使用預設值 ~ default parameters，算是某個參數在函數內會被用到，但是不見得要指派值，就可以使用預設值，常常會用在某些函數就是呼叫時有些參數通常都是使用某個值。像是下面的例子就是假設有一個函數會畫圈圈，可能圈圈邊邊的寬度通常是1，所以在

      ```typescript
      function drawCircle(radius: number, color: string, strokeWidth: number = 1) {
        // ,,, 忽略
        console.log(radius, color, strokeWidth);
      }
      
      // 10 'red' 5
      drawCircle(10, "red", 5);
      
      // 10 'red' 1
      drawCircle(10, "red");
      ```

      default parameter的位置沒有限制因為生成js的方式
      實現方式如下，就在函數body的一開始處生程式碼，確定如果沒初始化就給預設值

      ```typescript
      "use strict";
      function drawCircle(radius, color, strokeWidth) {
          if (radius === void 0) { radius = 5; }   // 用來檢查radius是否為undefined，如果是就給預設值
          if (strokeWidth === void 0) { strokeWidth = 1; } // 用來檢查strokeWidth是否為undefined，如果是就給預設值
          // ,,, 忽略
          console.log(radius, color, strokeWidth);
      }
      ```

   3. 有些參數的數量不固定 ~ rest parameters

      1. 注意事項 : rest parameter只能有一個而且只能放在最後面

      2. 語法

         ```typescript
         (arg1: type1, ...arg2: type2[]) // rest parameter的型別一定是陣列
         ```

      3. 範例

         ```typescript
         function printNumbers(msg: string, ...numbers: number[]) {
           console.log(msg, ...numbers);
         }
         // haha 1 2 3 4
         printNumbers("haha", 1, 2, 3, 4);
         ```

      4. 實現方式，會宣告一個陣列numbers存不固定數量的參數，會使用javascript的函數內特有的arguments陣列，將第二個參數後的都放到numbers陣列

         ```typescript
         function printNumbers(msg) {
             var numbers = [];
             for (var _i = 1; _i < arguments.length; _i++) {
                 numbers[_i - 1] = arguments[_i];
             }
             console.log.apply(console, __spreadArrays([msg], numbers));
         }
         ```

   4. generator和iterator

      1. generator是一個函數，他是惰性求值的函數，概念應該是從functional programming中來的，惰性求值就是沒有需要就不會求，像是如果有一個函數用來求質數，函數可以寫成沒有上限的找質數，呼叫一次會回傳下一個質數的值，也就是呼叫一次算一個，需要的時候才求值

         1. generator這個函數會回傳一個Generator物件，物件中有next()函數，會在函數內執行到遇到yield敘述，然後拿到回傳值回到原本執行的位置。

         2. 例子，會持續生成0,1,2,3,...的值的generator函數(如果沒有惰性求值，會花無窮的時間)

            ```typescript
            function* infinite() {
                let index = 0;
            
                while (true) { // 無窮迴圈
                    yield index++;
                }
            }
            
            const generator = infinite(); // "Generator { }"
            
            console.log(generator.next().value); // 0
            console.log(generator.next().value); // 1
            console.log(generator.next().value); // 2
            ```

         3. 語法

            函數宣告

            ```typescript
            function* functionName() {} // generator function在宣告時要function* xxx，要多個*號
            ```

            中斷的地方，回到原本執行的地方並回傳值的敘述為yield

            ```typescript
            yield index++;
            ```

         4. 概念

            就是可以反覆地進入某個函數得到值或執行某些動作

      2. iterator

         1. 就是可以讓物件被遍歷的函數

         2. 可以藉由iterable protocol來定義自己想要的迭代行為，像是在使用`for ... of `的時候會依序有哪些值，有些物件像是Array和Map已經有定義預設的迭代行為。

         3. 會定義在物件的Symbol.iterator這個property上

         4. 範例

            ```typescript
            const iterable1 = {};
            
            iterable1[Symbol.iterator] = function* () {
              yield 1; // 回傳1且回到原本執行的地方
              yield 2; // 回傳2原本執行的地方
              yield 3; // 回傳3回到原本執行的地方
            };
            
            console.log([...iterable1]);
            // expected output: Array [1, 2, 3]
            ```

      ## 類別

      1. 很多東西跟c++一樣像是方法和變數會有存取修飾子像是public、protected、private，繼承的關鍵字不一樣，typescript使用extends，下面舉個例，西洋棋的某個棋子都是Piece，對於每個棋子而言，移動到某個位置要做的事情一定都一樣，而能不能移動到哪個位置的函數一定都不一樣，所以定義會如下。King繼承Piece的moveTo，然後要實現canMoveTo函數

         ```typescript
         abstract class Piece {
             // ...
             moveTo(position: Position) {  // 每個棋子的移動作的事情都是改position，所以就直接定義在Piece這個抽象類別
                 this.position = position
             }
             abstract canMoveTo(position: Position): boolean // 因為還不知道是哪種棋子所以不知道要怎麼實作，因此用abstract，強迫繼承Piece的 
                                                             // class要實現canMoveTo這個函數
         }
         class King extends Piece {
             canMoveTo(position: Position) {
                 let distance = this.position.distanceFrom(position)
                 return distance.rank < 2 && distance.file < 2
             }
         } 
         ```

      2. super();
         在子類別的建構式中呼叫此函數會呼叫parent class的建構式

      3. 類別內的方法可以回傳this，也就是自身的實體(instance)的參考，用處就是可以作為fluent interface，可以一直呼叫，像是Set這個集合物件，有add可以加資料進去，還有has可以確定有沒有某個資料，add函數回傳this的話，就可以xxx.add(xxx).add(xxx).add(xxx)

         ```typescript
         let set = new Set
         set.add(1).add(2).add(3) // 目前set有1,2,3
         ```

## 介面(interface)

1. 有趣的部分 : interface的存在在於定義shape，只有型沒有值，只會用於typescript在編譯的時候作檢查用途，實際上不會產生任何程式碼

2. interface v.s. type

   1. 相同處

      1. 比較單純宣告interface和type的情況

         interface

         ```typescript
         interface SushiInterface {
           calories: number;
           salty: boolean;
           tasty: boolean;
         }
         ```

         type

         ```typescript
         type SushiType = {
           calories: number;
           salty: boolean;
           tasty: boolean;
         };
         ```

         這兩種做法之後生出來的javascript code都一樣

         typescript

         ```typescript
         type SushiType = {
           calories: number;
           salty: boolean;
           tasty: boolean;
         };
         
         interface SushiInterface {
           calories: number;
           salty: boolean;
           tasty: boolean;
         }
         
         let sushi: SushiType = {
           calories: 123,
           salty: true,
           tasty: true,
         };
         
         let sushi2: SushiInterface = {
           calories: 123,
           salty: true,
           tasty: true,
         };
         
         ```

         生出來的javascript

         ```javascript
         "use strict";
         let sushi = {
             calories: 123,
             salty: true,
             tasty: true,
         };
         let sushi2 = {
             calories: 123,
             salty: true,
             tasty: true,
         };
         
         ```

      2. 在根據現有的type或interface擴充，不完全重新描述全部的內容，只加入相異處，加上一些屬性而言，兩者相同，一個是用&(type)一個是用extends(interface)像是如下
         有三種東西Food、Sushi、Cake，Food很明顯比較抽象，所以屬於食物的Sushi和Cake會繼承Food的屬性

         ```typescript
         type Food = {
           calories: number;
           tasty: boolean;
         };
         
         type Sushi = {
           calories: number; // 與Food重複
           tasty: boolean; // 與Food重複
           salty: boolean; // 多的
         };
         
         type Cake = {
           calories: number; // 與Food重複
           tasty: boolean; // 與Food重複
           sweet: boolean; // 多的
         };
         ```

         用type和&可以改寫成

         ```typescript
         type Sushi = Food & {
             salty: boolean;
         }
         
         type Cake = Food & {
             sweet: boolean;
         }
         ```

         用interface和extends可以改寫成

         ```typescript
         interface Sushi extends Food {
             salty: boolean;
         }
         
         interface Cake extends Food {
             sweet: boolean;
         }
         ```

         > &和extends都是結合兩者，新的東西兩者都需要有

   2. 相異處

      1. type aliases(型別別名)(待解釋)

      2. interface在extends後，會檢查擴展的結果是可以指派值的，像是如下

         ```typescript
         interface A {
             good(x: number): string
             bad(x: number): string
         }
         
         interface B extends A {
             good(x: string | number): string
             bad(x: string): string // 這裡會出問題因為參數的型別沒有交集，number & string = 空的
         }
         ```

         就good函數而言，其signature從「number與 string | number」做&(兩者都有)得到string | number

         就bad函數而言，其signature從number&string，不可能兩者都有，x不是number就是string，不可能同時是這兩個，所以會有問題

      3. 在同一個scope的interface反覆宣告的結果會是，讓那些宣告結合在一起

3. Declaration Merging

   ```typescript
   interface User {
       name: string
   }
   // 目前User只有一個欄位name
   interface User {
       age: number
   }
   // 因為在同個scope下多次宣告同一個名稱的interface，所以會將兩者結合，目前User有兩個欄位name和age
   let a: User = {
       name: 'Ashley',
       age: 30
   }
   ```

4. Implementations(實作)

   1. 概念: 介面的用處有限制物件的屬性欄位和其型別也就是shape，除了這個用處之外還有一個就是interface的屬性欄位有可能是定義方法與其signature，而且那就會涉及到`其他語言的interface`，像是c#的interface就是一個介面，不會定義實作的內容，只會有函數名稱和signature，目的就在於彈性，透過介面互動，介面可以由許多class實現，這樣就不用獨立各自跟許多class溝通或是有介面不統一，在切換或呼叫的時候要寫不同的程式碼來達成，然後interface在typescript中也有類似的概念

   2. 範例

      ```typescript
      interface Animal {
          eat(food: string): void
          sleep(hours: number): void
      }
      
      class Cat implements Animal {
          eat(food: string) { // 在Animal interface中有定義
              cnosole.info('Ate some', food, '. Mmm!')
          }
          sleep(hours: number) {  // 在Animal interface中有定義
              console.info('Slept for', hours, 'hours')
          }
      }
      ```

   3. 特別之處 : 一個class可以實作多個介面

   4. 注意之處 : 一旦實作某個介面就要定義那個介面所有的東西的實作，不然會有問題

5. Implementing interfaces Versus Extending Abstract Classes

   1. 概念分析: interface可以定義函數與其signature(參數與回傳值)，然後讓class實作；然後abstract class可以有abstract method，只需定義不須實作，留給之後extends它的class實作，在這一點上面兩者幾乎一樣，然而在另一個層面interface比abstract輕量，像是之前有提過interface只會用作於編譯時期作檢查用途，所以interface輕量到不會影響到最後runtime的程式，而abstract class還是一個class，還是會產生javascript code，然後abstract class可以定義某些函數的預設實作、屬性的存取修飾(public、private、protected)，

6. classes are structurally Typed(類別以結構定型)

   1. 概念 : typescript就只在乎shape不在乎名稱，像是兩個class的shape都一樣，這樣如果有一個函數在定義時只接受其中一個，實際運行時兩個都會被接受。這跟其他c++那類的語言不一樣

      > typescript在比較class差異時只考慮結構相不相同，不在乎名稱，所以結構相同會被視為一樣的

   2. 範例

      ```typescript
      class A {
        private x = 1
      }
      class B extends A {} // 和A的結構完全一樣(shape一樣)
      function f(a: A) {}
      
      f(new A)   // OK
      f(new B)   // OK!!!!因為結構一樣，會被視為跟A一樣
      ```

7. Classes Declare Both Values and Types(類別會宣告值也會宣告型別)(超怪????之後再了解)

8. Polymorphism

   1. 跟泛型有關，這就跟typescript的generic type息息相關，因為可以在runtime時帶入任何型別

   2. generic type語法

      ```typescript
      class className<T1,T2> {
          // ...
      }
      
      // 使用時
      functionName(arg1: T1, arg2: T2) { // ... }
      ```

   3. 注意事項

      1. 在class階層宣告的generic type可以在所有class實體的方法和屬性出現
      2. class內的static method不能使用class階層宣告的generic type，因為只在實體出現，static是綁在class上的，不是在實體上的
      3. class內的method可以宣告和使用自己的generic type

## 錯誤處理(handling errors)

錯誤處理的作法有很多種，每種作法都有優點和缺點

1. Returning null

   像是在處理日期字串的時候，發現字串不符合特定的格式，這時可以回傳null，代表又問題，缺點就是要每次在使用函數回傳的值前要作檢查，大致如下

   ```typescript
   let returnValue = fun(xxx); // 函數回傳值可能會因為一些例外情況發生所以會是null
   if (returnValue) {
       console.log(returnValue)
   } else {
       // returnValue是null，發生錯誤了
       console.log('Error from fun')
   }
   ```

   > 優點: 很輕量簡單
   >
   > 缺點: 要特別去檢查函數的回傳值是否為null，而且不知道實際發生在函數的哪個位置，而且很難用chain operation

   chain operation

   ```typescript
   func1().func2().func3() // 無法作null回傳值的檢查
   ```

2. Throwing exceptions

   ```typescript
   function parse(birthday: string): Date {
     let date = new Date(birthday)
     if (!isValid(date)) {
       throw new RangeError('Enter a date in the form YYYY/MM/DD') // 當日期不符合格式就拋出錯誤
     }
     return date
   }
   
   // 當try block發生錯誤會由catch block處理然後繼續執行不會crash
   try {
     let date = parse(ask())
     console.info('Date is', date.toISOString())
   } catch (e) {
     console.error(e.message)
   }
   ```

   > 優點: 可以了解詳細的錯誤原因和錯在哪個位置
   >
   > 缺點: 如果沒有try~catch~到就會上整個程式中斷crash掉，然後可能

3. Returning exceptions

   在parse的return type那邊要加上錯誤類型，因為可能回傳，還有之後處理result時要處理每種類型的錯誤

   ```typescript
   function parse(
     birthday: string
   ): Date | InvalidDateFormatError | DateIsInTheFutureError {
     let date = new Date(birthday)
     if (!isValid(date)) {
       return new InvalidDateFormatError('Enter a date in the form YYYY/MM/DD')
     }
     if (date.getTime() > Date.now()) {
       return new DateIsInTheFutureError('Are you a timelord?')
     }
     return date
   }
   
   let result = parse(ask()) // Either a date or an error
   if (result instanceof InvalidDateFormatError) { // 處理日期格式的錯誤
     console.error(result.message)
   } else if (result instanceof DateIsInTheFutureError) { // 處理日期在未來的錯誤
     console.info(result.message)
   } else {
     console.info('Date is', result.toISOString())
   }
   ```

   > 優點: 可以在函數的signature也就是回傳值那邊可以看到可能發生哪些exception、可以強制讓使用者去處理每種類型的exceptions
   >
   > 缺點:  函數呼叫可能會func1呼叫func2，這樣一來func1要處理func2的錯誤以及回傳值的類型又多了func2的錯誤，會讓程式變的更冗長

4. The Option type

## Asynchronous Programming, Concurrency, and Parallelism

1. 概念 : javascript最初是在瀏覽器上運行的程式語言，所以在設計上需要考量到能夠不等待network資源的存取以及UI操作時能以非同步的方式處理，這樣才不會卡住。因為javascript是單執行緒的，所以要使用event queue，依序讓任務執行一小段時間，達到任務的time sharing

2. callback

   簡單的callback結構，ajax是非同步函數

   ```javascript
   // A
   ajax("..", function(...) {
       // C
   })
   // B
   ```

   A會先執行，然後在一般情況下B執行後才會執行C，C會等ajax完成在呼叫，這就是callback

   `callback hell`

   ```javascript
   async1((err1, res1)=> {
       if (res1) {
           async2(res1, (err2, res2) => {
               if (res2) {
                   async3(res3, (err3, res3) => {
                       // ...
                   })
               }
           }
       }
   })
   ```

3. promise用來解決callback的問題

   原本是要`將callback函數作為函數的參數傳入`變為能夠`回傳一個可以附上callback的物件`，這樣就不會有nested callback的問題(callback hell)![Understanding Method Chaining In Javascript | by Segun Ola ...](https://miro.medium.com/max/1772/1*s-OlfkC2Y1zg9m8S4rUlWQ.png)

   最基本的結構

   ```javascript
   const promise = createAudioFileAsync(audioSettings);
   promise.then(successCallback, failureCallback);
   ```

   Promise.prototype.then函數，讓promise可以chainning的關鍵，因為一定會回傳Promise，回傳的Promise又可以呼叫Promise.prototype.then函數，這樣就可以形成chaining

   



## 一些瑣碎問題的探討

1. this到底是什麼東西(蠻複雜的)

   1. 概念 : 算是context，也就是原本呼叫函數的時候會需要傳入一些變數，如果沒有this，如果要記錄呼叫函數幾次，就要有一個global variable，然後在函數中修改那個global variable的值，這樣每次都要傳入那個變數很不方便，這時候就會需要一個更方便的東西，也就是執行的context，誰呼叫它，this就是哪個物件

   2. 各種情境

      1. 在任何函數外的地方，this代表global context，如果在瀏覽器執行環境就會是window物件

      2. 如果是在函數內，this就是要取決於誰呼叫那個函數

         1. 如果定義一個物件alpha，物件中有屬性是函數，通常那個函數的this就是指alpha(因為呼叫函數一定要透過alpha物件，alpha.xxx(xxx))

            ```javascript
            const test = {
                prop: 42,
                func: function() {
                    return this.prop; // 因為後面呼叫的時候會是用test物件呼叫，所以this會是test物件，this.prop會存取到test物件的prop屬性
                },
            };
            
            console.log(test.func()); // 42
            ```

         2. 如果直接呼叫函數(沒透過一個中間人去存取)，this會是window物件，如果有使用xxx.call(xxx)函數則可以改變this為call的那個物件

            ```javascript
            function test() {
              console.log("test", this);
            }
            
            test(); // 在瀏覽器執行環境會是window物件
            
            var me = {
              name: "test",
            };
            
            test.call(me); // 將執行的context替換成me物件，因此this會是me物件，會印出test { name: 'test' }
            ```

            > 三個function prototype method : call、apply、bind，用在改變函數呼叫時的this為特定物件

            call

            ```javascript
            func.call(thisArg)
            func.call(thisArg, arg1, arg2, arg3, ...argN)
            // thisArg就是要作為this的東西
            // arg1, arg2, ...argN就是要給函數的參數
            ```

            apply

            ```javascript
            func.apply(thisArg)
            func.apply(thisArg, argsArray)
            // func執行時的this會變成thisArg
            // 跟call的差別在於參數傳入時是傳一個陣列(argsArray)
            ```

            bind

            ```javascript
            let boundFunc = func.bind(thisArg)
            let boundFunc = func.bind(thisArg, arg1, arg2, ...argN)
            // 概念就是把函數包裹在另一個函數，然後提拱想要的執行context，之後就呼叫boundFunc，好處就是之後呼叫就直接用boundFunc，不需要每次都要用    call或apply，怕會忘記之類的
            // boundFunc執行時this會變成thisArg
            // arg1, arg2, ...argN是傳給函數的參數
            ```

      3. 在類別中this跟函數一樣，要取決於誰呼叫，通常都是指類別實體化成的物件，不過使用call、bind那類的東西會改變this

### 暫時問題集

1. 一般宣告函數語法內的this context是什麼 v.s. arrow function函數宣告的this context是什麼
2. javascript的closure是什麼

