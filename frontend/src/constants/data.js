import images from "./images";

export const what_we_do = [
        {
        image: `${images.konsol4}`,
        title: 'Compare Game Prices and Save Money!',
        paragraph: 'We all want to buy our favorite games at the best prices, don\'t we? That\'s where we come in! Our website brings together prices from popular platforms like Steam, Epic Games, and GOG, making it easy for you to compare them. No more hopping between platforms to check prices—we’ve got you covered. Simply search for the game you want, and see the prices from the three major platforms displayed on one screen. Game shopping has never been this easy or smart. Plus, with regular updates during sale periods, we ensure you never miss out on the best deals!'
        },
    
        {
            image: `${images.konsol5}`,
            title: 'Get Your Favorite Games at the Best Prices!',
            paragraph: 'The gaming world is constantly changing, and so are the prices. Whether Steam is having a massive sale or Epic Games is giving away free games, we\'re here to help you find the best deals. Our website is your ultimate guide. For example, if you\'re planning to buy GTA V but aren\'t sure where it\'s the cheapest, just visit our site and find out in seconds! Spend less time researching and more time gaming. Saving money and shopping smart has never been easier!'
        },
]

export const features = [
    {
        icon: `${images.featuresIcon1}`,
        title: 'Thousands of Games Just a Click Away!',
        text: 'From action and adventure to strategy and more! Explore the gaming universe and find your perfect match..'
    },
    {
        icon: `${images.save}`,
        title: 'Save Big with Exclusive Deals!',
        text: 'Enjoy massive discounts on top-rated games. Check out our daily deals and grab your favorite games at unbeatable prices.'
    },
    {
        icon: `${images.download}`,
        title: 'Download and Play Instantly!',
        text: 'No waiting time! Buy your favorite game and start playing within minutes with our instant digital delivery system.'
    },
    {
        icon: `${images.game}`,
        title: 'Games for Every Device!',
        text: 'Find games for PC, console, and mobile. Whatever your platform, we\'ve got you covered.'
    },
    {
        icon: `${images.click}`,
        title: 'Thousands of Games Just a Click Away!',
        text: 'From action and adventure to strategy and more! Explore the gaming universe and find your perfect match..'
    },
    {
        icon: `${images.help}`,
        title: 'We are Here to Help Anytime!',
        text: 'Got a question or an issue? Our dedicated support team is available around the clock to assist you.'
    },
]

const packages = [
    {
        type: 'Basic',
        service_list: [
            'only 5 games search',
            'you can watch 5 game video',
        ],
        price: '100'
    },
    {
        type: 'Standard',
        service_list: [
            'Only 10 Games Search',
            'You can watch 10 game video',
        ],
        price: '150'
    },
    {
        type: 'Premium',
        service_list: [
            'Only 15 Games Search',
            'You can watch 15 game video',
        ],
        price: '200'
    },
]
export const projects = [
    {
        image: `${images.slider2}`,
        title: 'Logo Design',
    }
]
const teams = [
    {
        image: `${images.user1}`,
        name: "Batuhan Kaya",
        post: "Backend - Frontend Developer"
    },
    {
        image: `${images.user4}`,
        name: "Hüseyin Can Kayım",
        post: "Backend Developer"
    },
    {
        image: `${images.user5}`,
        name: "Kadir Emre Güral",
        post: "Backend - Database Developer"
    }
]


const data = { what_we_do, features, packages, projects, teams };
export default data;