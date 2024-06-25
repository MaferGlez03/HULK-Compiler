# Expressions

HULK is ultimately an expression-based language. Most of the syntactic constructions in HULK are expressions, including the body of all functions, loops, and any other block of code.

The body of a program in HULK always ends with a single global expression (and, if necessary, a final semicolon) that serves as the entrypoint of the program. This means that, of course, a program in HULK can consist of just one global expression.

For example, the following is a valid program in HULK:

```js
42;
```

Obviously, this program has no side effects. A slightly more complicated program, probably the first one that does something, is this:

```js
print(42);
```

In this program, `print` refers to a builtin function that prints the result of any expression in the output stream. We will talk about functions in a later section.

The rest of this section explains the basic expressions in HULK.

## Arithmetic expressions

HULK defines three types of literal values: **numbers**, **strings**, and **booleans**.
We will leave strings and booleans for later.

Numbers are 32-bit floating-point and support all basic arithmetic operations with the usual semantics: `+` (addition), `-` (subtraction), `*` (multiplication), `\` (floating-point division), `^` (power), and parenthesized sub-expressions.

The following is a valid HULK program that computes and prints the result of a rather useless arithmetic expression:

```js
print((((1 + 2) ^ 3) * 4) / 5);
```

All usual syntactic and precedence rules apply.

## Strings

String literals in HULK are defined within enclosed double-quotes (`"`), such as in:

```js
print("Hello World");
```

A double-quote can be included literally by escaping it:

```js
print("The message is \"Hello World\"");
```

Other escaped characters are `\n` for line endings, and `\t` for tabs.

Strings can be concatenated with other strings (or the string representation of numbers) using the `@` operator:

```js
print("The meaning of life is " @ 42);
```

## Builtin math functions and constants

Besides `print`, HULK also provides some common mathematical operations encapsulated as builtin functions with their usual semantics. The list of builtin math functions is the following:

- `sqrt(<value>)` computes the square root if a value.
- `sin(<angle>)` computes the sine of an angle in radians.
- `cos(<angle>)` computes the cosine of an angle in radians.
- `exp(<value>)` computes the value of `e` raised to a value.
- `log(<base>, <value>)` computes the logarithm of a value in a given base.
- `rand()` returns a random uniform number between 0 and 1 (both inclusive).

Besides these functions, HULK also ships with two global constants: `PI` and `E` which represent the floating-point value of these mathematical constants.

As expected, functions can be nested in HULK (provided the use of types is consistent, but so far all we care about is functions from numbers to numbers, so we can forget about types until later on). Hence, the following is a valid HULK program.

```js
print(sin(2 * PI) ^ 2 + cos(3 * PI / log(4, 64)));
```

More formally, function invocation is also an expression in HULK, so everywhere you expect an expression you can also put a call to builtin function, and you can freely mix arithmetic expressions and mathematical functions, as you would expect in any programming language.

## Expression blocks

Anywhere an expression is allowed (or almost), you can also use an expression block, which is nothing but a series of expressions between curly braces (`{` and `}`), and separated by `;`.

The most trivial usage of expression blocks is to allow multiple `print` statements as the body of a program. For example, the following is a valid HULK program:

```js
{
    print(42);
    print(sin(PI/2));
    print("Hello World");
}
```

When you use an expression block instead of a single expression, it is often not necessary to end with a semicolon (`;`), but it is not erroneous to do so either.

# Functions

HULK also lets you define your own functions (of course!). A program in HULK can have an arbitrary number of functions defined before the final global expression (or expression block).

A function's body is always an expression (or expression block), hence all functions have a return value (and type), that is, the return value (and type) of its body.

## Inline functions

 The easiest way to define a function is the inline form. Here's an example:

```js
function tan(x) => sin(x) / cos(x);
```

An inline function is defined by an identifier followed by arguments between parenthesis, then the `=>` symbol, and then a simple expression (not an expression block) as body, ending in `;`.

In HULK, all functions must be defined before the final global expression. All these functions live in a single global namespace, hence it is not allowed to repeat function names. Similarly, there are no overloads in HULK (at least in "basic" HULK).

Finally, the body of any function can use other functions, regardless of whether they are defined before or after the corresponding function. Thus, the following is a valid HULK program:

```js
function cot(x) => 1 / tan(x);
function tan(x) => sin(x) / cos(x);

print(tan(PI) ** 2 + cot(PI) ** 2);
```

And of course, inline functions (and any other type of function) can call themselves recursively.

## Full-form functions

Since inline functions only allow for a single expression as body (as complex as that may be), HULK also allows full-form functions, in which the body is an expression block.

Here's an example of a rather useless function that prints 4 times:

```js
function operate(x, y) {
    print(x + y);
    print(x - y);
    print(x * y);
    print(x / y);
}
```

Note that the following form is discouraged for stylistic reasons:

```js
function id(<args>) => {
    <...>
}
```

That is, you should either use the inline form with `=>` and a simple expression, or the full form with `{}` and an expression block.

# Variables

Variables in HULK are lexically-scoped, which means that their scope is explicitely defined by the syntax. You use the `let` expression to introduce one or more variables in and evaluate an expression in a new scope where does variables are defined.

The simplest form is introducing a single variable and using a single expression as body.

```js
let msg = "Hello World" in print(msg);
```

Here `msg` is a new symbol that is defined *only* within the expression that goes after `in`.

## Multiple variables

The `let` expression admits defining multiple variables at once like this:

```js
let number = 42, text = "The meaning of life is" in
    print(text @ number);
```

This is semantically equivalent to the following long form:

```js
let number = 42 in
    let text = "The meaning of life is" in
        print(text @ number);
```

As you can notice, `let` associates to the right, so the previous is also equivalent to:

```js
let number = 42 in (
    let text = "The meaning of life is" in (
            print(text @ number)
        )
    );
```

## Scoping rules

Since the binding is performed left-to-right (or equivalently starting from the outer let), and every variable is effectively bound in a new scope, you can safely use one variable when defining another:

```js
let a = 6, b = a * 7 in print(b);
```

Which is equivalent to (and thus valid):

```js
let a = 6 in
    let b = a * 7 in
        print(b);
```

## Expression block body

You can also use an expression block as the body of a `let` expression:

```js
let a = 5, b = 10, c = 20 in {
    print(a+b);
    print(b*c);
    print(c/a);
}
```

As we said before, semicolons (`;`) are seldom necessary after an expression block, but they are never wrong.

## The `let` return value

As with almost everything in HULK, `let` is an expression, so it has a return value, which is obviously the return value of its body. This means the following is a valid HULK program:

```js
let a = (let b = 6 in b * 7) in print(a);
```

Or more directly:

```js
print(let b = 6 in b * 7);
```

This can be of course nested ad infinitum.

## Redefining symbols

In HULK every new scope hides the symbols from the parent scope, which means you can redefine a variable name in an inner `let` expression:

```js
let a = 20 in {
    let a = 42 in print(a);
    print(a);
}
```

The previous code prints `42` then `20`, since the inner `let` redefines the value of `a` inside its scope, but the value outside its still the one defined by the outer `let`.

And because of the [scoping rules](#scoping-rules), the following is also valid:

```js
let a = 7, a = 7 * 6 in print(a);
```

Which is equivalent to:

```js
let a = 7 in
    let a = 7 * 6 in
        print(a);
```

## Destructive assignment

Most of the time in HULK you won't need to overwrite a variable, but there are cases where you do. In those cases, you can use the destructive assignment operator `:=`, like this:

```js
let a = 0 in {
    print(a);
    a := 1;
    print(a);
}
```

The previous program prints `0` and then `1`, since the value of `a` is overwritten before the second `print`.
This is the **only** way in which a variable can be written to outside of a `let`.

As you would expect, the `:=` operator defines an expression too, which returns the value just assigned, so you can do the following:

```js
let a = 0 in
    let b = a := 1 in {
        print(a);
        print(b);
    };
```

This is useful if you want to evaluate a complex expression to both test it (e.g, to se if its greater than zero) and store it for later use.

# Conditionals

The `if` expression allows evaluating different expressions based on a condition.

```js
let a = 42 in if (a % 2 == 0) print("Even") else print("odd");
```

Since `if` is itself an expression, returning the value of the branch that evaluated true, the previous program can be rewritten as follows:

```js
let a = 42 in print(if (a % 2 == 0) "even" else "odd");
```

Conditions are just expressions of boolean type. The following are the valid boolean expressions:

- Boolean literals: `true` and `false`.
- Arithmetic comparison operators: `<`, `>`, `<=`, `>=`, `==`, `!=`, with their usual semantics.
- Boolean operators: `&` (and), `|` (or), and `!` (not) with their usual semantics.

## Expression blocks in conditionals

The body of the `if` or the `else` part of a conditional (or both) can be an expression block as well:

```js
let a = 42 in
    if (a % 2 == 0) {
        print(a);
        print("Even");
    }
    else print("Odd");
```

## Multiple branches

The `if` expression supports multiple branches with the `elif` construction, which introduces another conditioned branch:

```js
let a = 42, let mod = a % 3 in
    print(
        if (mod == 0) "Magic"
        elif (mod % 3 == 1) "Woke"
        else "Dumb"
    );
```
# Loops

HULK defines two kinds of loops, the `while` expression and the `for` expression.
Both loop constructions are expressions, returing the value of the

## The `while` loop

A `while` loop evaluates a condition and its body while the condition is true. The body can be a simple expression or an expression block.

```js
let a = 10 in while (a >= 0) {
    print(a);
    a := a - 1;
}
```

Since the return value of the `while` loop is the return value of its expression body, it can often be used directly as the body of a function.

```js
gcd(a, b) => while (a > 0)
    let m = a % b in {
        b := a;
        a := m;
    };
```

## The `for` loop

A `for` loop iterates over an _iterable_ of elements of a certain type. We will [talk about iterables](/iterables) later on, but for now it suffices to say that if some expression evaluates to a collection, then the `for` loop can be used to iterate it.

For example, the builtin `range(<start>, <end>)` function evaluates to an iterable of numbers between `<start>` (inclusive) and `<end>` (non-inclusive).

```js
for (x in range(0, 10)) print(x);
```

The `for` loop is semantically and operationally equivalent to the following:

```js
let iterable = range(0, 10) in
    while (iterable.next())
        let x = iterable.current() in
            print(x);
```

In fact, what the reference implementation of the HULK compiler does in `for` loops is to transpile them into their `while` equivalent. This also effectively means that, just like the `while` loop, the `for` loop returns the last value of its body expression.
# Types

HULK is ultimately an object-oriented language with simple inheritance and nominal typing. It also has features of structural typing via [protocols](/protocols), which support language features such as [iterables](/iterables), which we will explain later.

This section explains the basics of HULK's nominal typing system.

A type in HULK is basically a collection of attributes and methods, encapsulated under a type name. Attributes are always private, which means they can't be read or writen to from any code outside the type in which they are defined (not even inheritors), while methods are always public and virtual.

## Declaring types

A new type is declared using the `type` keyword followed by a name, and a body composed of attribute definitions and method definitions. All attributes must be given an initialization expression. Methods, like functions, can have a single expression or an expression block as body;

```js
type Point {
    x = 0;
    y = 0;

    getX() => self.x;
    getY() => self.y;

    setX(x) => self.x := x;
    setY(y) => self.y := y;
}
```

The body of every method is evaluated in a namespace that contains global symbols plus an especial symbol named `self` that references the current instance. The `self` symbol is **not** a keyword, which means it can be hidden by a `let` expression, or by a method argument.

However, when referring to the current instance, `self` is not a valid assignment target, so the following code should fail with a semantic error:

```js
type A {
    // ...
    f() {
        self := new A(); // <-- Semantic error, `self` is not a valid assignment target
    }
}
```

## Instantiating types

To instantiate a type you use the keyword `new` followed by the type name:

```js
let pt = new Point() in
    print("x: " @ pt.getX() @ "; y: " @ pt.getY());
```

As you can see, type members are accessed by dot notation (`instance.member`).

You can pass arguments to a type, that you can use in the initialization expressions. This achieves an effect similar to having a single constructor.

```js
type Point(x, y) {
    x = x;
    y = y;

    // ...
}
```

Then, at instantiation time, you can pass specific values:

```js
let pt = new Point(3,4) in
    print("x: " @ pt.getX() @ "; y: " @ pt.getY());
```

Each attribute initialization expression is evaluated in a namespace that contains the global symbols and the type arguments, but no the `self` symbol. This means you cannot use other attributes of the same instance in an attribute initialization expression. This also means that you cannot assume any specifc order of initialization of attributes.

## Inheritance

Types in HULK can inherit from other types. The base of the type hierarchy is a type named `Object` which has no public members, which is the type you implicitely inherit from by default. To inherit from a specific type, you use the `inherits` keyword followed by the type name:

```js
type PolarPoint inherits Point {
    rho() => sqrt(self.getX() ^ 2 + self.getY() ^ 2);
    // ...
}
```

By default, a type inherits its parent type arguments, which means that to construct a `PolarPoint` you have to pass the `x` and `y` that `Point` is expecting:

```js
let pt = new PolarPoint(3,4) in
    print("rho: " @ pt.rho());
```

If you want to define a different set of type arguments, then you have to provide initialization expressions for the parent type at the declaration:

```js
type PolarPoint(phi, rho) inherits Point(rho * sin(phi), rho * cos(phi)) {
    // ...
}
```

During construction, the expressions for type arguments of the parent are evaluated in a namespace that contains global symbols plus the type arguments of the inheritor. Like before, you cannot assume a specific order of evaluation.

In HULK, the three builtin types (`Number`, `String`, and `Boolean`) implicitely inherit from `Object`, but it is a semantic error to inherit from these types.

## Polymorphism

All type methods in HULK are virtual by definition, and can be redefined by an inheritor provided the exact same signature is used:

```js
type Person(firstname, lastname) {
    firstname = firstname;
    lastname = lastname;

    name() => self.firstname @@ self.lastname;
}
```

> **NOTE**: `@@` is equivalent to `@ "  " @`. It is a shorthand to insert a whitespace between two concatenated strings. There is no `@@@` or beyond, we're not savages.

```js
type Knight inherits Person {
    name() => "Sir" @@ base();
}

let p = new Knight("Phil", "Collins") in
    print(p.name()); // prints 'Sir Phil Collins'
```

The `base` symbol in every method refers to the implementation of the parent (or the closest ancestor that has an implementation).

# Type checking

HULK is a statically-typed language with optional type annotations. So far you haven't seen any because HULK has a powerful [type inference system](/inference) which we will talk about later on. However, all symbols in HULK have a static type, and all programs in HULK are statically checked during compilation.

Tye annotations can be added anywhere a symbol is defined, that is:

- in variable declarations with `let` expressions;
- in function or method arguments and return type;
- in type attributes; and,
- in type arguments.

Let's see an example of each case.

## Typing variables

Variables can be explicitely type-annotated in `let` expressions with the following syntax:

```js
let x: Number = 42 in print(x);
```

The type checker will verify that the type inferred for the initialization expression is compatible with (formally, [conforms to](/#type-conforming)) the annotated type.

## Typing functions and methods

All or a subset of a function's or method's arguments, and its return value, can be type-annotated with a similar syntax:

```js
function tan(x: Number): Number => sin(x) / cos(x);
```

On the declaration side, the type checker will verify that the body of the method uses the types in a way that is consistent with their declaration. The exact meaning of this consistency is defined in the section about [type semantics](/type_semantics). The type checker will also verify that the return type of the body conforms to the annotated return type.

On the invocation side, the type checker will verify that the values passed as parameters conform to the annotated types.

Inside methods of a type `T`, the implicitly defined `self` symbol is always assumed as if annotated with type `T`.

## Typing attributes and type arguments

In type definitions, attributes and type arguments can be type-annotated as follows:

```js
type Point(x: Number, y: Number) {
    x: Number = x;
    y: Number = y;

    // ...
}
```

The type checker will verify that type arguments are used consistently inside attribute initialization expressions, and that the inferred type for each attribute initialization expression conforms to the attribute annotation.

## Type conforming

The basic type relation in HULK is called *conforming* (`<=`). A type `T1` is said to *conform to* to another type `T2` (writen as `T1 <= T2`) if a variable of type `T2`  can hold a value of type `T1` such that every possible operation that is semantically valid with `T2` is guaranteed to be semantically valid with `T1`.

In general, this means that the type checker will verify that the inferred type for any expression conforms to the corresponding type declared for that expression (e.g., the type of a variable, or the return type of a function).

The following rules provide an initial definition for the *conforming* relationship. The formal definition is given in the section about [type semantics](/type_semantics).

- Every type conforms to `Object`.
- Every type conforms to itself.
- If `T1` inherits `T2` then `T1` conforms to `T2`.
- If `T1` conforms to `T2` and `T2` conforms to `T3` then `T1` conforms to `T3`.
- The only types that conform to `Number`, `String`, and `Boolean`, are respectively those same types.

Types in HULK form a single hierarchy rooted at `Object`. In this hierarchy the *conforming* relationship is equivalent to the *descendant* relationship. Thus, if `T1` conforms to `T2` that means that `T1` is a descendant of `T2` (or trivially the same type). Thus, we can talk of the lowest common ancestor of a set of types `T1`, `T2`, ..., `Tn`, which is the most specific type `T` such that all `Ti` conform to `T`. When two types are in different branches of the type hierarchy, they are effectively incomparable.

> **NOTE**: this conforming relationship is extended when we add [protocols](./protocols).

## Testing for dynamic types

The `is` operator allows to test an object to check whether its dynamic type conforms to a specific static type.

```js
type Bird {
    // ...
}

type Plane {
    // ...
}

type Superman {
    // ...
}

let x = new Superman() in
    print(
        if (x is Bird) "It's bird!"
        elif (x is Plane) "It's a plane!"
        else "No, it's Superman!"
    );
```

In general, before the `is` operator you can put any expression, not just a variable.

## Downcasting

You can use the `as` operator to downcast an expression to a given static type. The result is a runtime error if the expression is not a suitable dynamic type, which means you should always test if you're unsure:


```js
type A {
    // ...
}

type B inherits A {
    // ...
}

type C inherits A {
    // ...
}

let x : A = if (rand() < 0.5) new B() else new C() in
    if (x is B)
        let y : B = x as B in {
            // you can use y with static type B
        }
    else {
        // x cannot be downcasted to B
    }
```
# Type inference

Since every program in HULK is statically type-checked, and type annotations are optional in most cases, this means that HULK infers types for most of the symbols in a program.

Because the problem of type inference is computationally complex, and ultimately unsolvable in the general case, the HULK reference definition doesn't give precise semantics about how the type inferer must work. Rather, we will give only a set of minimal constraints that the type inferer must assert if a type is inferred at all for a given symbol, or otherwise it must fail to infer types.

## Type inference vs type checking

The type inferer works before the type checker, and assigns type annotations to all symbols that are not explicitly annotated, and to all the expressions. Afterwards, the type checker verifies that all semantic rules are valid.

Thus, even if a program is fully annotated, the type inferer still needs to work, since it needs to infer the type of all expressions. When some symbols are not explicitly annotated, the type inferer must also assign types for them.

Hence, there are two different moments when a semantic error can be reported. First, if the type inferer cannot infer the type of some symbol, a semantic error will be thrown to indicate the programmer that some symbol must be explicitly typed. Second, if the type inferer finished without errors, the type checker will verify that all types are consistent, and will report a semantic error if there is some incompatibilty.

## Type inference of expressions

The first task of the type inferer is to infer the runtime type of any expression that appears in a HULK program. This process is performed bottom-up, starting from atomic sub-expressions (e.g., literals) and working up the AST. The exact rules for type inference of expressions is given in the section a`bout [type semantics](/type_semantics), but an intuitive introduction can be given at this point.

Literals are the easiest to type-infer, because their type comes directly from the parser. Arithmetic expressions are also easy, because their type is always `Number`. Likewise, string and boolean operators are straightforward.

The type of complex expressions that have an expression body is determined by the type of the body. This is the case of `let`, `while`, and `for`. The type of an expression block is the type of the last expresion of the block. The type of a function or method invocation is the type of its body. The type of expressions that have more than one branch (`if`) is the lowest common ancestor of the types of each branch, or ultimately `Object`.

## Type inference of symbols

Once all expressions have been type-inferred, the type inferer will attempt to assing a type to each symbol declaration that is not explicitly annotated. Instead of providing an exact algorithm, we will define a set of constraints that the type inferer must satisfy whenever it succeeds in assigning a type.

Specific implementations of HULK can choose different methods to attempt the type inference of symbols. According to the order in which symbols are processed, and the sophistication of each method, some implementations may succed where others fail. However, if two type inference algorithms are correct, they most agree on all types for which both succeed in the inference.

These are the constraints a type inference algorithm must satisfy to be correct, or otherwise it must report a failed inference.

- In a `let` expression, whenever a variable is not type-annotated, the type inferer must asign a type for the variable that is equivalent to the type infered for its initialization expression.
- Similarly, in an attribute declaration that is not type-annotated, the type inferer must assign a type that is equivalent to the type inferred for its initialization expression.
- In a function or method, whenever an argument is not type-annotated, the type inferer must assign the lowest (most specific) type that would be consistent with the use of that argument in the method or function body. If more than one type in different branches of the type hierarchy would be consistent, the type inferer must fail.
- Similarly, in a type argument, the type inferer must assign the lowest type that is consistent with the use of that argument in all attribute initialization expressions where it is referenced.

If a type inferer satisfies those constraints, we will say it is *sound*. This means that, for example, the simplest sound strategy for type inference is to infer types for all expressions and fail for all symbols. We will call this the *basic inference* strategy.

## Examples of type inference

These are some programs where a sufficiently sophisticated type inference strategy should work.

In the following program the type of the variable `x` should be inferred to `Number` because the type of `42` is trivially `Number`:

```js
let x = 42 in print(x);
```

In the following function, the type of the argument `n` should be inferred as `Number` because it is the only possible type where arithmetic operators (i.e., `+`) are defined, as there is no operator overloading in HULK:

```js
function fib(n) => if (n == 0 | n == 1) 1 else fib(n-1) + fib(n-2);
```

For the same reason, in the following function, the type of the argument `x` should be inferred as `Number`. Likewise, the type of the variable `f` should be inferred as `Number` because the initialization expression is a literal `Number`.

```js
function fact(x) => let f = 1 in for (i in range(1, x+1)) f := f * i;
```

> **TODO**: Add more examples...

# Protocols

Protocols are special types which support a limited form of structural typing in HULK. The difference between structural and nominal typing in HULK, is that the latter is explicit while the former is implicitely defined. That is, a type doesn't need to explicitely declare that it conforms to a protocol.

Protocols have a syntax similar to that of types, except that they only have method declarations, and they have no body, only signatures. Hence, protocols define the methods that a type must have in order to support some operation.

Protocols don't exist at runtime, they are compile-time only concept that helps writing more flexible programs. After type checking, all information about protocols can be safely removed.

## Defining protocols

A protocol is defined with the keyword `protocol` followed by a collection of method declarations:

```js
protocol Hashable {
    hash(): Number;
}
```

A protocol can have any number of method declarations. For obvious reasons, all method declarations in protocol definitions must be fully typed, as it is impossible to infer any types since they have no body.

A protocol can extend anoter protocol by adding new methods, but never overriding (since there is no actual body) or removing any method.

```js
protocol Equatable extends Hashable {
    equals(other: Object): Boolean;
}
```

## Implementing protocols

A type implements a protocol implicitely, simply by having methods with the right signature. There is no need to explicitely declare which types implement which protocols.

Thus, you can annotated a variable or argument with a protocol type, and the type checker will correctly verify the consistency of both the method body and the invocation.

```js
type Person {
    // ...

    hash() : Number {
        // ...
    }
}

let x : Hashable = new Person() in print(x.hash());
```

Anywhere you can annotate a symbol with a type (variables, attributes, function,method and type arguments, and return values), you can also use a protocol. For the purpose of type inference, protocols are treated as types.

## Covariance and contravariance in protocol implementation

In order to implementing a protocol, a type doesn't necessarily have to match the exact signature of the protocol. Instead, method and type arguments are considered *contravariant*, and return values *covariant*. This means that arguments can be of the same type or higher, and the return values of the same type or lower than as defined in the protocol.

# Iterables

An iterable in HULK is any object that follows the iterable protocol, which is defined as follows:

```js
protocol Iterable {
    next() : Boolean;
    current() : Object;
}
```

An example of iterable is the builtin `range` function, which returns an instance of the builtin `Range` type, defined as follows:

```js
type Range(min:Number, max:Number) {
    min = min;
    max = max;
    current = min - 1;

    next(): Boolean => (self.current := self.current + 1) < max;
    current(): Number => self.current;
}
```

Notice that since protocols are covariant in the return types of the methods, the `Range` type correctly implements the `Iterable` protocol.

## Using iterables with the `for` loop

As explained in [the loops section](/loops), the `for` loop works with the `Iterable` protocol, which means you can apply `for` on any instance of a type that implements the protocol.

In compile-time, `for` is transpiled to a code that is equivalent, but explicitely uses the `Iterable` protocol members.

For example, the code:

```js
for (x in range(0,10)) {
    // code that uses `x`
}
```

Is transpiled to:

```js
let iterable = range(0, 10) in
    while (iterable.next())
        let x = iterable.current() in {
            // code that uses `x`
        }
```

This transpilation guarantees that even though the `Iterable` protocol defines the `current` method with return type `Object`, when you use a `for` loop you will get the exact covariant type inferred in `x`.

As a matter of fact, due to the transpilation process, the `Iterable` protocol itself is not even necessary, since nowhere is a symbol annotated as `Iterable`. However, the protocol is explicitely defined as a builtin type so that you can explicitly use it if you need to annotate a method to receive a black-box iterable.

Keep in mind, thought, that when you annotate something explicitely as `Iterable`, you are effectively forcing the type inferrer to assign `Object` as the type of the iteration variable (`x` in this example). This is one of the  reasons it is often better to let HULK infer types than annotating them yourself.

## Typing iterables
# Vectors

The builtin vector type provides a simple but powerful abstraction for creating collections of objects of the same type. In terms of functionality, a vector is close to plain arrays as defined in most programming languages. Vectors implement the [iterable protocol](/iterables) so they can be iterated with a `for` syntax.

Vectors in HULK can be defined with two different syntactic forms: explicit and implicit.

## Explicit syntax

An explicit vector of `Number`, for example, can be defined as follows:

```js
let numbers = [1,2,3,4,5,6,7,8,9] in
    for (x in numbers)
        print(x);
```

Because vectors implement the iterable protocol, you can explicitely find a `next` and `current` methods in case you ever need them. Besides that, vectors also have a `size(): Number` method that returns the number of items in the vector.

Vectors also support an indexing syntax using square brackets `[]`, as in the following example:

```js
let numbers = [1,2,3,4,5,6,7,8,9] in print(numbers[7]);
```

## Implicit syntax

An implicit vector can be created using what we call a generator pattern, which is always an expression  Here's an example:

```js
let squares = [x^2 | x in range(1,10)] in print(x);
// prints 2, 4, 6, 8, 10, ...
```

## Typing vectors

Actually, there is not one single `Vector` type in HULK, at least not in a way that is accesible from HULK code.