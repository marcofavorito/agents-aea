The AEA framework consists of several core elements, some of which are required to run an AEA and others which are optional.

## The advanced elements AEAs use

In <a href="../core-components-1">Core Components - Part 1</a> we discussed the elements each AEA uses. We will now look at some of the advanced elements each AEA uses.

### Decision Maker

<img src="../assets/decision-maker.jpg" alt="Decision Maker of an AEA" class="center" style="display: block; margin-left: auto; margin-right: auto;width:50%;">

The <a href="../api/decision_maker/base#decisionmaker-objects">`DecisionMaker`</a> can be thought of as a `Wallet` manager plus "economic brain" of the AEA. It is responsible for the AEA's crypto-economic security and goal management, and it contains the preference and ownership representation of the AEA. The decision maker is the only component which has access to the `Wallet`'s private keys.

You can learn more about the decision maker <a href="../decision-maker">here</a>. In the simplest form, it acts like a `Handler` with a `Wallet`.

### Wallet

The <a href="../api/crypto/wallet#wallet-objects">`Wallet`</a> contains the private-public key pairs used by the AEA. Skills do not have access to the wallet, only the decision maker does.

### Identity

The <a href="../api/identity/base#identity-objects">`Identity`</a> is an abstraction that represents the identity of an AEA in the Open Economic Framework, backed by public-key cryptography. It contains the AEA's addresses as well as its name.

The identity can be accessed in a `Skill` via the <a href="../api/context/base#agentcontext-objects">`AgentContext`</a>.

## Optional elements AEAs use

### Contracts

<img src="../assets/contracts.jpg" alt="Contracts of an AEA" class="center" style="display: block; margin-left: auto; margin-right: auto;width:50%;">

<a href="../api/contracts/base#contract-objects">`Contracts`</a> wrap smart contracts for third-party decentralized ledgers. In particular, they provide wrappers around the API or ABI of a smart contract. They expose an API to abstract implementation specifics of the ABI from the `Skills`.

`Contracts` usually contain the logic to create contract transactions.

`Contracts` can be added as packages. For more details on `Contracts` also read the `Contract` guide <a href="../contract">here</a>.

## Putting it together

Taken together, the core components from this section and the <a href="../core-components-1">first part</a> provide the following simplified illustration of an AEA:

<img src="../assets/simplified-aea.jpg" alt="Simplified illustration of an AEA" class="center" style="display: block; margin-left: auto; margin-right: auto;width:100%;">

## Next steps

### Recommended

We recommend you continue with the next step in the 'Getting Started' series:

- <a href="../generic-skills-step-by-step/">Trade between two AEAs</a>

### Relevant deep-dives

Understanding the decision maker is vital to developing a goal oriented and crypto-economically safe AEA. You can learn more about the `DecisionMaker` in the following section:

- <a href="../decision-maker">Decision Maker</a>


Understanding `Contracts` is important when developing AEAs that make commitments or use smart contracts for other aims. You can learn more about the `Contracts` agents use in the following section:

- <a href="../contract">Contracts</a>


<br />

