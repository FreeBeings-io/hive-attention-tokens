  
# Hive Attention Tokens (HAT)

*This is a work in progress, please feel free to contribute to the discussion on [Hive](https://hive.blog/@freebeings).*

Hive Attention Tokens is a proposed layer 2 token protocol for the Hive blockchain, to allow dApps to create their own tokens and monetize their platforms using the Hive blockchain.

It is designed to utilize the Hive Application Framework to maintain state currently, but will ultimately be ported to a native Hive smart contract when the Hive blockchain supports smart contracts.

When creating a new token, there are a number of properties that you can set to determine how your token comes into existence and how it will behave over time.

- **Simple Attention Tokens** are fixed supply, “dumb” tokens, which are suitable for tipping, community voting rights, access rights or other use cases that do not need automatic distribution based on the wisdom of the crowd.

- **Wisdom of Crowd Tokens** are smart tokens with a configurable elastic supply, automated distribution and vote based distribution features. These tokens are suitable for monetizing dApps, where the value of the token is correlated to the number of users (and possibly type of demographics) using the dApp.

---

## Simple Attention Token (Overview)

Tokens will have a fixed supply and the whole supply is defined at creation and no new tokens will ever be created.

-   non-inflationary
-   send/burn to spend
-   send with expiration timestamp

### Token Creation

Properties to set:

- initial_supply: the number of tokens that will be created

- control_account: usually the same as the account that creates the token, but can be another account.

- initial_distribution: the Hive accounts to which tokens are to be sent at creation, useful for airdrops. As an example, a content creator can allocate all distribution to their own account, for use as an NFT for accessing special content.

---

## Wisdom of Crowd Token (Overview)

These are tokens whose supply increases over time, with new tokens being distributed to a rewards pool and optionally a development fund.

-   Emission rate: set how many new tokens are created over time
-   Emission distribution: choose where the new tokens go and the ratios of allocation between the rewards pool and development fund

To control the initial distribution, token creators have the option to allocate tokens to specific Hive accounts at the point of creation. Once the number of initial tokens is set, a supply property has to be chosen.

### Token Creation

Properties to set:

-   initial_supply
-   emission_rate
-   rewards_fund
-   development_fund
-   initial_distribution
-   airdrop_list: a `transaction_id` property, which links to a `custom_json` operation containing the list of Hive accounts and the number of tokens to send to each, and when to send them
- claimdrop: a `transaction_id` property, which links to a `custom_json` operation containing the total amount of tokens available for the claimdrop and how much to allocate to each claiming account
-   effective operations

**Note:**

The `airdrop_list` and `claimdrop` properties are optional and can be used to distribute tokens to users automatically after token creation. The `airdrop_list` property is used to distribute tokens to users at the point of creation, while the `claimdrop` property is used to distribute tokens to users at a later time, when the users claim.


### Rewards Pool

This is a virtual account that holds tokens to be distributed to user accounts as part of the monetization of a dApp. This account will be useful also for dApps whose tokenomics are designed to bootstrap the value of the token through an attention economy.

As an example, users can spend their tokens to gain visibilty on the platform. Setting this account as the account for payments, creates a virtuous cycle where the more users spend their tokens, the more tokens are distributed back to the rewards pool, which in turn is distributed to users.

### Development Fund

An optional development fund can be enabled by token creators, to enable the long term funding of their efforts from the supply of the created token. A voting system can be enabled to allow token holders to vote on the continued supply of this fund and to which account it should be directed.

### Token staking [WIP]

Tokens can be staked to a Hive account, to allow the account to vote within the token's ecosytem for governance purposes. This will be optional and up to the dApp developers to design their own token's governance system, if needed.

More research is planned to determine the best way to implement this feature.

---

## Native HAT transactions


### Broadcast Properties

HAT Properties can be attached to user operations. These will add additional user-side metadata to HAT, such as beneficiary accounts and percentages.

### Custom JSON Operations

Support for `custom_json` based interactions will be added to HAT, to allow dApps and their users to interact with HAT, to broadcast intent to vote or set beneficiaries for rewardable content or actions created using `custom_json` operations.

### Comment Operations

The `comment` operations can also interact with HAT, to allow users to set beneficiaries for rewardable content. These properties can be added to the `json_metadata` property of the `comment` operation.

---

## Algorithms

We propose that HAT smart tokens not use stake-weighted voting alone, but rely more on a combination of algorithms designed to mimic social interactions in real life.

### Content Tracking Algorithm

To reward content, a unique content tracking algorithm is needed. Hive posts can already be uniquely tracked, but dApps that use `custom_json` operations for content broadcasting need to be supported. dApps will use their own content tracking and to have HAT support this, we propose an algorithm that allows token creators to define which unique data is used in their applications.

To achieve this, JSON paths are used, with support for:

- operation versioning, to allow future upgrades of the algorithm by control accounts
- one or two unique fields for content tracking

For example, if an app uses a `custom_json` payload to broadcast the creation of a post similar to this one:  

{
    "title": "My first post",  
    "body": "This is my first post",  
    "tags": ["hive", "hat"],
    "permlink": "my-first-post"
}

The corresponding HAF entry for this operations will be similar to this:

{
    "type": "custom_json_operation",
    "value": {
        "required_auths": [],
        "required_posting_auths": ["user.cool"],
        "id": "my_app",
        "json": [
            [1, "my_app/1.0.0"],
            "create_post",
            {
                "title": "My first post",  
                "body": "This is my first post",  
                "tags": ["hive", "hat"],
                "permlink": "my-first-post"
            }
        ]
    }
}

The JSON paths recorded will be:

- version: `$.value.json[0][0]`
- author: `$.value.required_posting_auths[0]`
- permlink: `$.value.json[2].permlink`

This will be used to track unique content and reward it. An example database entry for this would be:

{
    "hat_token": "0000000000000000000000000000000000000000",
    "source": "custom_json_operation",
    "version": 1,
    "author": "user.cool",
    "permlink": "my-first-post"
}

### Social Distance Algorithm

We propose a social distance algorithm that will be used to determine how far one user is away from the network of the user affected by their operation. This weighted distance could be calculated using the amount of interactions between the two users, or the amount of time that has passed since the last interaction for example.

This aims to mitigate the effects of unwarranted downvotes by users who are not part of the same network as the user being downvoted.

**Technical details:**


Variables:

- `content` - the content being voted on
- `user` - the user who created the content
- `actor` - the user who is voting
- `following` - whether or not the actor is following the user
- `actor_interaction_score` - the number of interactions between the actor and the user
- `actor_interaction_bias` - the bias towards the actor's interactions with the user (positive vs negative)
- `actor_distance` - the resultant distance between the actor and the user

Formula Description:

- calculate the total number of interactions between the actor and the user
- calculate the bias of the actor's interactions with the user (positive vs negative)
    - if the actor has more positive interactions with the user, the bias is positive
    - if the actor has more negative interactions with the user, the bias is negative
- actor_distance is:
    - actor's interaction score as a fraction of the total interaction scores of other actors to the same user
    - weighted by the actor's interaction bias (important for accounting for actors who are distancing themselves from the user)
    - weighted by the actor's following status, where following weighs more than not following


Illustrative Formula:

*This is an illustrative formula, not the actual formula used in the implementation.*

    actor_distance = (actor_interaction_score / total_interaction_score) * actor_interaction_bias * following_weight

    following_weight = following ? 1.5 : 1

### Reputation Algorithm

We propose a reputation algorithm that uses the weighted balance of positive and negative interactions between users to determine a reputation score.

The score will be an emergent property, calculated from the balance mentioned above and also influenced by the social distance algorithm to an extent.

In effect, this aims to make the reputation score a reflection of how well a user's content or actions are being received by their network and then use that score as a main factor in the distribution of rewards.

**Technical details:**

Variables:

- `actor_interaction_scores` - the number of interactions between the actor and the user, daily, fibonaccially weighted
- `actor_distance` - the distance between the actor and the user
- `user_reputation` - the resultant reputation of the user

Formula Description:

- calculate the total number of interactions between the actor and the user, daily, fibonaccially weighted
- calculate the distance between the actor and the user
- user_reputation is:
    - the total number of interactions between the actor and the user, daily, fibonaccially weighted
    - weighted by the distance between the actor and the user

Illustrative Formula:

*This is an illustrative formula, not the actual formula used in the implementation.*

    user_reputation = (actor_interaction_scores * actor_distance) * historical_reputation

### Token distribution Algorithm

This will use the results from the reputation algorithm above to determine the amount of tokens to distribute to each user, dynamically, based on the amount of tokens in the rewards pool.

In effect, a user's reputation will directly influence how much of the rewards pool their posts will receive, versus other user's reputations. So if a user's reputation is negatively impacted in recent days, their posts will receive less rewards.

**Technical details:**

Variables:

- `content` - the content being voted on
- `user` - the user who created the content
- `actor` - the user who is voting
- `actor_reputation` - the reputation of the actor
- `user_reputation` - the reputation of the user
- `reward_impact` - the votes weight versus all votes cast that day
- `rewards_pool` - the amount of tokens in the rewards pool
- `revenue_share` - the percentage of the rewards pool to be distributed to the user

Formula Description:

- calculate the reputation of the actor
- calculate the reputation of the user
- calculate the reward impact: the votes weight versus all votes cast that day, weighted by the actor's and user's reputation
- calculate the percentage of the rewards pool to be distributed to the user, revenue share is:
    - the reward impact as a fraction of the total reward impact of all other active users

## Sybil Attack Mitigation

We propose the optional use of verified account operations, to add the account to a list of human verified accounts in line with the policies of the dApp itself. This could be done by the control account of the token itself or by accounts delegated by the control account to onboard users.

An option to enable verified access to the token's ecosystem will be added to the token creation process.

On the other hand, we also propose the use of a moderation system, with flagging operations, made by both regular dApp users and accounts delegated by the control account of the token.

THe ultimate operation being a demotion operation, to allow dApp users to inhibit the distribution of rewards to accounts that are not behaving in line with the policies of the dApp or community. This operation could be performed by the control account of the token itself or by accounts delegated by the control account to moderate the platform.

Since reputation will be a key factor in the distribution of rewards, such flagging operations will negatively affect the reputation of a user, which will in turn affect the distribution of rewards to bad actors attempting to game the system. Repeated offences would eventually lead to the demotion of the account.