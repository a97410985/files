# Typescript 學習心得

## 與其他語言不同的地方

1. 選擇性參數

   雖然很多語言都有提供 **預設參數**

   ```typescript
   function hello(name: string = "World") {
     console.log(`Hello ${name}!`);
   }
   ```

   但是都沒有提供**選擇性參數**

   ```typescript
   function hello(name?: string) {
     console.log(`Hello ${name || "World"}!`);
   }
   ```

2. `this`

   c++裡面也有 `this`指標，但是跟 c++很不同的是，typescript 可以在 function 直接使用`this`而 c++不行

   ```typescript
   function logDate(this: Date) {
     console.log(`${this.getDate()}/${this.getMonth()}/${this.getFullYear()}`);
   }
   // function 本身沒有this.getDate()等東西，必須bind一個有getDate()的物件才能使用，這邊有特別指定要bind Date類型的物件
   logDate.call(new Date());
   ```

   ```typescript
   //如果沒有bind直接使用則會報錯
   //The 'this' context of type 'void' is not assignable to method's 'this' of type 'Date'.
   logDate();
   ```

3. overloaded function

   跟 C++的 function overloading 很不同的一點是，C++在宣告函式時只要宣告同名以及不同的參數就好，呼叫時就會自動根據參數型態來決定呼叫的函式，而且 function 的內容是分別定義

   ```c++
   void foo(int x) {
     cout << "int 引數：" << x << endl;
     cout << "我可以比較不一樣~" << endl;
   }
   void foo(double x) {
     cout << "double 引數：" << x << endl;
   }
   ```

   而 typescript 的 function overloading 則是只宣告不同的參數類型以及回傳類型

   ```typescript
   function logSomething(something: string): string;
   function logSomething(something: number): number;
   function logSomething(something: boolean): boolean;
   function logSomething(something: any): any {
     console.log(something);
     return something;
   }
   ```

   typescript 如果想要做到跟 C++相似的不同數量參數則可以同時使用選擇性參數+重載來實現

   ```typescript
   function logSomething(something: string): string;
   function logSomething(something: number): number;
   function logSomething(something: boolean, time: Date): boolean; // 兩個參數
   function logSomething(something: any, time?: Date | string): any {
     console.log(something);
     if (time) {
       console.log(time);
     }
     return something;
   }
   ```

4. `null`, `undefined`, `never`

   ```typescript
   // null 通常代表值的缺席
   class LinkedListNode {
     private value: number;
     private next: LinkedListNode;
     constructor(val: number) {
       this.value = val;
       this.next = null; // 這邊的null是代表沒有指向的 LinkedListNode 而非 "尚未定義"
     }
     newNode(val: number) {
       const _newNode = new LinkedListNode(val);
       let current = this;
       while (current.next !== null) {
         current = current.next;
       }
       current.next = _newNode;
     }
   }
   // undefined 代表尚未定義
   let variable; //宣告但是並未指定值時的值就會是 undefined
   // never 代表永遠不會回傳的函式
   function runForever(): never {
     while (true) {}
   }
   function alwaysError(): never {
     throw new Error("I am always error!");
   }
   ```

5. 物件的多重繼承

   C++如果要實作多重繼承，會是像下面程式碼：

   ```C++
   class C: public A, public B{
   public:
       C(int x): A(x), B(x){
        // do something
       }
       // do something
   }
   ```

   而 typescript 則是要

   ```typescript
   class C {
     // do somthing
   }
   interface C extends A, B {}
   applyMixins(SmartObject, [Person, Student]);

   function applyMixins(derivedCtor: any, baseCtors: any[]) {
     baseCtors.forEach((baseCtor) => {
       Object.getOwnPropertyNames(baseCtor.prototype).forEach((name) => {
         Object.defineProperty(
           derivedCtor.prototype,
           name,
           Object.getOwnPropertyDescriptor(baseCtor.prototype, name)
         );
       });
     });
   }
   ```

6. `interface`, `type`

   在建立物件時，想要為某個物件產生一種類型時，就會用到`interface`或`type`

   ```typescript
   function printCourseDetails(course: {
     name: string;
     calories: number;
     price: number;
   }) {
     //過於壟長
     console.log(`${course.name}: ${course.calories}卡, ${course.price}`);
   }
   // type
   type Course = {
     name: string;
     calories: number;
     price: number;
   };
   // interface
   interface Course {
     name: string;
     calories: number;
     price: number;
   }
   function printCourseDetails(course: Course) {
     console.log(`${course.name}: ${course.calories}卡, ${course.price}`);
   }
   ```

## typescript 類別與其他語言相似的地方

1. 修飾詞 `public`, `protected`, `private`

   跟 java 還有 C++一樣，都可以對屬性以及方法進行修飾，限制對屬性或方法的存取

   ```typescript
   class Account {
     constructor(public username: string, private password: string) {}
     public sayHello(): void {
       console.log("Hello!");
     }
     private explosion(): void {}
   }

   let alice = new Account("Alice", "@l1ce");
   console.log(alice.username);
   console.log(alice.password); // error, can only be access by class 'Account'
   alice.sayHello();
   alice.explosion(); // error, can only be access by class 'Account'
   ```

2. 抽象類別( **Abstract Class** )

   跟 java 還有 C++一樣，可以先建立一個未定義完全的類別，但是無法直接實體化該類別

   ```typescript
   abstract class Animal {
     constructor(public name: string) {}
     abstract sound(): string;
   }
   let sheep = new Animal("Sheep"); // error, cannot create an instance of an abstract class
   ```

   必須在子類別實做 abstract 方法才能實體化

   ```typescript
   class Sheep extends Animal {
     sound() {
       return "咩~";
     }
   }
   let sheep = new Sheep("Sheep");
   ```

## 介面 (interface)

1. interface 擴充 ( **extends** )

   ```typescript
   interface User {
     name: string;
   }
   interface Admin extends User {
     role: string;
   }
   ```

2. 宣告合併

   若是宣告了多個一樣名字的 interface，且 interface 互相不衝突，如下：

   ```typescript
   interface User {
     name: string;
   }
   interface User {
     age: number;
   }
   ```

   則會 typescript 會幫我們自動將他們結合成為一個 interface，所以當我們這時候使用 User 這個 interface 的時候就會是像下面的 interface

   ```typescript
   interface User {
     name: string;
     age: number;
   }
   ```

   如果 interface 互相衝突的話呢?

   ```typescript
   interface User {
     age: string;
   }
   interface User {
     age: number;
   } // error, 'age' must be of type 'string'
   ```

3. 實作 ( **implements** )

   實作跟類別的繼承有點像，但是需要實作 interface 的每個方法，而且跟繼承不一樣的是，一個 class 可以實作多個 interface！

   ```typescript
   interface Animal {
     eat(food: string): void;
     sleep(hours: number): void;
   }
   interface Feline {
     meow(): void;
   }
   class Cat implements Animal, Feline {
     eat(food: string): void {
       console.log(`Eating ${food} ...`);
     }
     sleep(hours: number): void {
       console.log(`Ready to sleep for ${hours}hours...`);
     }
     meow(): void {
       console.log("Meow~");
     }
   }
   ```

## typescript 的錯誤處理

1. 回傳 null

   方法：如果錯誤就回傳 null

   優點：處理錯誤最輕量化的方法

   缺點：

   1. 會喪失一些資訊，不知道為何會引發這樣的錯誤。
   2. 編寫困難

2. 擲出例外

   方法：

   ```typescript
   return new RangeError("Enter a date in the form YYYY/MM/DD");
   ```

   使用函式時則要捕捉例外：

   ```typescript
   try {
     someFunction();
   } catch (e) {
     console.error(e.message);
   }
   ```

   只捕捉特定的例外：

   ```typescript
   try {
     someFunction();
   } catch (e) {
     if (e instanceof RangeError) {
       console.error(e.message);
     } else {
       throw e; // rethrow error
     }
   }
   ```

   缺點：工程師很懶，會懶得 try catch

3. 回傳例外
   方法：

   ```typescript
   return new RangeError("Enter a date in the form YYYY/MM/DD");
   ```

   處理例外：

   ```typescript
   let result = someFunction();
   if (result instanceof RangeError) {
     console.error(result.message);
   }
   ```

   優點：就算工程師很懶，也必須處理各個例外，因為不處理會報錯 XDDD

   缺點：如果把 Error 一直丟給耗用者處理，可能的錯誤清單可能會變的越來越長

4. Option 型別

   簡單來說，就是透過實作幾個 class 跟 function 來讓我們可以處理錯誤。

   1. function

      1. `flatMap(func)`

         可能的回傳值：

         |                     | Some\<T\>呼叫 | None 呼叫 |
         | ------------------- | ------------- | --------- |
         | func 回傳 Some\<U\> | Some\<U\>     | None      |
         | func 回傳 None      | None          | None      |

      2. `getOrElse(val)`

         可能的回傳值：
         | Some\<T\>呼叫 | None 呼叫 |
         | ------------- | --------- |
         | Some\<U\> | val|

      3. `Option(val)`

         可能的回傳值：
         |val | null \| undefined | 其他 |
         |------| ------------- | --------- |
         |return| None | Some\<T\>|

   2. 型別 / 類別

      1. `Some<T>`

      2. `None`

      3. `Option<T>`

         `Option<T> = Some<T> | None`

      使用範例：

      ```typescript
      // No error
      let result = Option(9)
        // function Option return => Some<number> (value = 9)
        .flatMap((n) => Option(n * 4))
        // function Option return => Some<number> (value = 36) and
        // flatMap also return the same thing because last value was not None
        .flatMap((n) => Option(n + 8))
        // function Option return => Some<number> (value = 44) and
        // flatMap also return the same thing because last value was not None
        .getOrElse(7);
      // function getOrElse return => Some<number> (value = 44) since last value was not None
      ```

      ```typescript
      // With error
      let result = Option(9)
        // function Option return => Some<number> (value = 9)
        .flatMap((n) => None)
        // flatMap return None because the function passed in always return None
        .flatMap((n) => Option(n * 4))
        // flatMap return None since last value was None
        .flatMap((n) => Option(n + 8))
        // flatMap return None since last value was None
        .getOrElse(7);
      // function getOrElse return 7 since last value was None
      ```

      由上面的範例可以看出，只要有連續運算有一個地方出錯，回傳了 None，就算後面的全部運算都是沒有錯誤的，也都會跟著回傳 None

      優點：處理連續運算的時候，使用上非常方便。

      缺點：跟回傳 null 一樣，無法得知哪邊出了錯誤。

## 非同步程式設計

1. callback

   callback 是非同步 javascript 程式最基本的單元

   範例：

   ```typescript
   async1((err1, res1) => {
     if (res1) {
       async2((err2, res2) => {
         if (res2) {
           async3((err3, res3) => {
             if (res3) {
               async4((err4, res4) => {
                 // do something
               });
             }
           });
         }
       });
     }
   });
   ```

   很明顯的，當你想要讓非同步程式運作得像同步程式一樣，會遇到一個很大的問題：

   程式會變得難以閱讀。而且上面的範例僅僅是用了 4 個 function 就變得如此複雜，可想而知，想再新增更多 function 會讓程式幾乎無法讀懂。

2. Promise

   在只有幾層的情況下， callback 或許還算是可以閱讀的，但多到一定程度後，就該 Promise 出場了，畢竟一定沒幾個人想看一堆縮排的程式碼 XDD

   範例：

   ```typescript
   function countdown(seconds: number): Promise<number> {
     return new Promise((resolve, reject) => {
       if (seconds === 9487) {
         return resolve(9487);
       } else {
         return reject(`Invalid number ${seconds}`);
       }
     });
   }
   let result = countdown(9487)
     .then((success) => {
       return countdown(success);
     })
     .then((success) => {
       return countdown(success);
     })
     .catch((e) => console.error(e));
   // result = 9487
   ```

   如範例，Promise 可以透過 then 一直串下去，錯誤也可以透過 catch 來捕捉。

3. async await

   範例：

   ```typescript
   // Promise
   function getUser() {
     getUserId(18)
       .then((user) => getLocation(user))
       .then((location) => console.info(`got location ${location}`))
       .catch((error) => console.error(error))
       .finally(console.info(`done getting location`));
   }
   // async / await
   async function getUser() {
     try {
       let user = await getUserId(18);
       let location = await getLocation(user);
       console.info(`got location ${location}`);
     } catch (error) {
       console.error(error);
     } finally {
       console.info(`done getting location`);
     }
   }
   ```

   如範例，Promise 樣子的 function 經過改寫之後就跟平常在寫得同步程式沒兩樣了。
